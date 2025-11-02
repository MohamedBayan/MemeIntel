#!/usr/bin/env python3
"""
Step 3: Merge batch results (generated explanations) with original dataset.

This version is specifically for explanation generation tasks.
It adds the generated explanation to each item in the original dataset.

Usage:
    python 3_merge_results_explanation.py \
        --dataset /path/to/original_dataset.jsonl \
        --results_dir ./results \
        --output ./dataset_with_explanations.jsonl
"""
import argparse
import json
import logging
import os


def setup_logging():
    """Configure logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def load_batch_results(results_dir):
    """Load all batch result files and extract generated explanations."""
    results = {}
    
    result_files = [f for f in os.listdir(results_dir) if f.startswith('batch_output_') and f.endswith('.jsonl')]
    
    logging.info(f"Found {len(result_files)} result files")
    
    for result_file in result_files:
        file_path = os.path.join(results_dir, result_file)
        
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    result = json.loads(line.strip())
                    custom_id = result['custom_id']
                    
                    # Extract the response content (should be JSON with explanation field)
                    if 'response' in result and 'body' in result['response']:
                        content = result['response']['body']['choices'][0]['message']['content']
                        
                        # Try to parse the JSON response
                        try:
                            # Clean up markdown code blocks if present
                            if content.strip().startswith('```'):
                                # Remove ```json or ``` at start and ``` at end
                                lines = content.strip().split('\n')
                                content = '\n'.join(lines[1:-1])
                            
                            parsed_content = json.loads(content.strip())
                            explanation = parsed_content.get('explanation', content)
                        except json.JSONDecodeError:
                            # If not valid JSON, use the raw content
                            logging.warning(f"Could not parse JSON for {custom_id}, using raw content")
                            explanation = content
                        
                        results[custom_id] = explanation
                        
                except Exception as e:
                    logging.warning(f"Error parsing result: {e}")
                    continue
    
    logging.info(f"Loaded {len(results)} generated explanations")
    return results


def merge_with_dataset(dataset_path, results, output_path):
    """Merge generated explanations with original dataset."""
    merged_count = 0
    total_count = 0
    
    with open(output_path, 'w', encoding='utf-8') as out_f:
        with open(dataset_path, 'r', encoding='utf-8') as in_f:
            for line in in_f:
                item = json.loads(line.strip())
                total_count += 1
                
                # Use the 'id' field from dataset to match with custom_id from results
                item_id = item.get('id', '')
                
                # Add generated explanation if available
                if item_id in results:
                    item['generated_explanation'] = results[item_id]
                    merged_count += 1
                else:
                    item['generated_explanation'] = None
                    logging.warning(f"No explanation found for item: {item_id}")
                
                out_f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    logging.info(f"Merged {merged_count}/{total_count} items with generated explanations")
    return merged_count, total_count


def main():
    parser = argparse.ArgumentParser(description='Merge batch results (explanations) with original dataset')
    parser.add_argument('--dataset', required=True, help='Path to original JSONL dataset')
    parser.add_argument('--results_dir', default='./results', help='Directory with batch results')
    parser.add_argument('--output', default='./dataset_with_explanations.jsonl', help='Output JSONL file')
    
    args = parser.parse_args()
    setup_logging()
    
    # Validate inputs
    if not os.path.exists(args.dataset):
        logging.error(f"Dataset not found: {args.dataset}")
        return
    
    if not os.path.exists(args.results_dir):
        logging.error(f"Results directory not found: {args.results_dir}")
        return
    
    # Load results
    logging.info("Loading batch results...")
    results = load_batch_results(args.results_dir)
    
    if not results:
        logging.error("No results found!")
        return
    
    # Merge with dataset
    logging.info("Merging generated explanations with original dataset...")
    merged_count, total_count = merge_with_dataset(args.dataset, results, args.output)
    
    logging.info(f"✓ Merge complete!")
    logging.info(f"  Output file: {args.output}")
    logging.info(f"  Success rate: {merged_count}/{total_count} ({100*merged_count/total_count:.1f}%)")
    
    if merged_count < total_count:
        logging.warning(f"  {total_count - merged_count} items missing explanations (may still be processing)")


if __name__ == "__main__":
    main()
