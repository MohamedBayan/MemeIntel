"""
Core batch processing library for multimodal inference.
"""
import base64
import json
import os
from openai import AzureOpenAI


class MultimodalBatchProcessor:
    def __init__(
        self,
        dataset_path,
        prompt_file,
        output_dir,
        batch_file_size_limit=180 * 1024 * 1024,
        image_size_limit=10 * 1024 * 1024,
    ):
        """
        Initialize the batch processor.

        Args:
            dataset_path (str): Path to the JSONL dataset file
            prompt_file (str): Path to the instruction prompt text file
            output_dir (str): Directory where batch files will be saved
            batch_file_size_limit (int): Maximum size of batch file in bytes (default: 180MB)
            image_size_limit (int): Maximum size of individual image in bytes (default: 10MB)
        """
        self.dataset_path = dataset_path
        self.prompt_file = prompt_file
        self.output_dir = output_dir
        self.batch_file_size_limit = batch_file_size_limit
        self.image_size_limit = image_size_limit
        
        # Load instruction prompt
        with open(self.prompt_file, 'r', encoding='utf-8') as f:
            self.instruction = f.read().strip()
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def load_dataset(self):
        """Load dataset from JSONL file."""
        data = []
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())
                # Validate required fields
                if 'img_path' in item:
                    data.append(item)
        return data

    def encode_image_base64(self, image_path):
        """Encode image to base64 string."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        with open(image_path, 'rb') as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded

    def get_image_size(self, image_path):
        """Get image file size in bytes."""
        return os.path.getsize(image_path)

    def create_request_payload(self, item, deployment_name):
        """
        Create API request payload for a single item.
        
        Format: <image> {instruction} Text extracted: {text}
        """
        img_path = item['img_path']
        text = item.get('text', item.get('extracted_text', ''))
        class_label = item.get('class_label', '')
        
        # Build the user message - substitute class_label into instruction if it contains {}
        instruction = self.instruction.format(class_label) if '{}' in self.instruction else self.instruction
        user_text = f"{instruction}\nText extracted: {text}"
        
        # Encode image
        base64_image = self.encode_image_base64(img_path)
        image_url = f"data:image/jpeg;base64,{base64_image}"
        
        # Use 'id' field from dataset if available, otherwise fall back to image basename
        custom_id = item.get('id', os.path.basename(img_path))
        
        # Create payload
        payload = {
            "custom_id": custom_id,
            "method": "POST",
            "url": "/chat/completions",
            "body": {
                "model": deployment_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url}
                            },
                            {
                                "type": "text",
                                "text": user_text
                            }
                        ]
                    }
                ],
                "max_tokens": 4096,
                "temperature": 0.0
            }
        }
        
        return payload

    def create_batches(self, deployment_name):
        """Create batch files from dataset."""
        dataset = self.load_dataset()
        current_batch = []
        current_batch_size = 0
        batch_counter = 1
        
        print(f"Processing {len(dataset)} items...")
        
        for item in dataset:
            img_path = item['img_path']
            
            # Check if image exists and is within size limit
            if not os.path.exists(img_path):
                print(f"Warning: Image not found: {img_path}")
                continue
                
            if self.get_image_size(img_path) > self.image_size_limit:
                print(f"Warning: Image too large (>10MB): {img_path}")
                continue
            
            try:
                # Create request payload
                payload = self.create_request_payload(item, deployment_name)
                payload_size = len(json.dumps(payload).encode('utf-8'))
                
                # Check if we need to start a new batch
                if current_batch_size + payload_size > self.batch_file_size_limit:
                    self.save_batch(current_batch, batch_counter)
                    current_batch = []
                    current_batch_size = 0
                    batch_counter += 1
                
                current_batch.append(payload)
                current_batch_size += payload_size
                
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
                continue
        
        # Save remaining items
        if current_batch:
            self.save_batch(current_batch, batch_counter)
        
        print(f"Batch creation complete. {batch_counter} batch files created.")

    def save_batch(self, batch, batch_counter):
        """Save batch to JSONL file."""
        batch_file_path = os.path.join(self.output_dir, f"batch_{batch_counter}.jsonl")
        with open(batch_file_path, 'w') as f:
            for item in batch:
                f.write(json.dumps(item) + '\n')
        print(f"Saved batch {batch_counter} with {len(batch)} items to {batch_file_path}")


class AzureBatchManager:
    def __init__(self, api_key, api_endpoint, api_version, deployment_name, batch_tracking_file):
        """
        Initialize Azure OpenAI Batch Manager.
        
        Args:
            api_key (str): Azure OpenAI API key
            api_endpoint (str): Azure OpenAI endpoint URL
            api_version (str): API version
            deployment_name (str): Model deployment name
            batch_tracking_file (str): File to track submitted batch IDs
        """
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=api_endpoint
        )
        self.deployment_name = deployment_name
        self.batch_tracking_file = batch_tracking_file

    def save_batch_id(self, batch_id, batch_file_path):
        """Save batch ID and file path to tracking file."""
        with open(self.batch_tracking_file, 'a') as f:
            f.write(f"{batch_id},{batch_file_path}\n")
        print(f"Batch ID {batch_id} saved for file {batch_file_path}")

    def submit_batch(self, batch_file_path):
        """Submit a single batch job."""
        try:
            # Upload batch file
            with open(batch_file_path, 'rb') as f:
                batch_input_file = self.client.files.create(file=f, purpose='batch')
            
            # Create batch job
            response = self.client.batches.create(
                input_file_id=batch_input_file.id,
                endpoint="/chat/completions",
                completion_window="24h",
                metadata={"description": f"Batch from {os.path.basename(batch_file_path)}"}
            )
            
            batch_id = response.id
            self.save_batch_id(batch_id, batch_file_path)
            print(f"Submitted batch {batch_id} from {batch_file_path}")
            
            return batch_id
            
        except Exception as e:
            print(f"Error submitting batch {batch_file_path}: {e}")
            return None

    def submit_all_batches(self, batch_dir):
        """Submit all batch files in directory."""
        batch_files = [f for f in os.listdir(batch_dir) if f.endswith('.jsonl')]
        print(f"Found {len(batch_files)} batch files to submit")
        
        for batch_file in batch_files:
            batch_path = os.path.join(batch_dir, batch_file)
            self.submit_batch(batch_path)

    def check_status(self, batch_id):
        """Check status of a batch job."""
        try:
            response = self.client.batches.retrieve(batch_id)
            return response.status
        except Exception as e:
            print(f"Error checking status for {batch_id}: {e}")
            return "error"

    def retrieve_results(self, batch_id, output_dir):
        """Retrieve results for a completed batch."""
        try:
            response = self.client.batches.retrieve(batch_id)
            
            if response.status == "completed":
                output_file = os.path.join(output_dir, f"batch_output_{batch_id}.jsonl")
                file_response = self.client.files.content(response.output_file_id)
                
                with open(output_file, 'w') as f:
                    f.write(file_response.text)
                
                print(f"Retrieved results for batch {batch_id}")
                return output_file
            else:
                print(f"Batch {batch_id} status: {response.status}")
                return None
                
        except Exception as e:
            print(f"Error retrieving results for {batch_id}: {e}")
            return None

    def retrieve_all_results(self, output_dir):
        """Retrieve all completed batch results."""
        if not os.path.exists(self.batch_tracking_file):
            print(f"No tracking file found: {self.batch_tracking_file}")
            return []
        
        result_files = []
        with open(self.batch_tracking_file, 'r') as f:
            for line in f:
                batch_id, _ = line.strip().split(',')
                status = self.check_status(batch_id)
                
                if status == "completed":
                    result_file = self.retrieve_results(batch_id, output_dir)
                    if result_file:
                        result_files.append(result_file)
                else:
                    print(f"Batch {batch_id} is {status}, skipping...")
        
        return result_files
