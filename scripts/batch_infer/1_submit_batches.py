#!/usr/bin/env python3
"""
Step 1: Create and submit batch jobs to Azure OpenAI.

Usage:
    python 1_submit_batches.py \
        --dataset /path/to/dataset.jsonl \
        --prompt /path/to/prompt.txt \
        --env_file .env \
        --output_dir ./batches
"""
import argparse
import logging
import os
from dotenv import load_dotenv
from batch_processor import MultimodalBatchProcessor, AzureBatchManager


def setup_logging():
    """Configure logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def load_env_variables(env_file):
    """Load Azure OpenAI credentials from env file."""
    load_dotenv(dotenv_path=env_file, override=True)
    
    return {
        'api_key': os.environ['AZURE_API_KEY'],
        'api_endpoint': os.environ['AZURE_API_URL'],
        'api_version': os.environ['AZURE_API_VERSION'],
        'deployment_name': os.environ['AZURE_ENGINE_NAME']
    }


def main():
    parser = argparse.ArgumentParser(description='Create and submit batch inference jobs')
    parser.add_argument('--dataset', required=True, help='Path to JSONL dataset file')
    parser.add_argument('--prompt', required=True, help='Path to instruction prompt text file')
    parser.add_argument('--env_file', required=True, help='Path to .env file with Azure credentials')
    parser.add_argument('--output_dir', default='./batches', help='Directory for batch files')
    parser.add_argument('--tracking_file', default='./batch_tracking.txt', help='File to track batch IDs')
    
    args = parser.parse_args()
    setup_logging()
    
    # Validate inputs
    if not os.path.exists(args.dataset):
        logging.error(f"Dataset not found: {args.dataset}")
        return
    
    if not os.path.exists(args.prompt):
        logging.error(f"Prompt file not found: {args.prompt}")
        return
    
    if not os.path.exists(args.env_file):
        logging.error(f"Environment file not found: {args.env_file}")
        return
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load credentials
    logging.info("Loading Azure OpenAI credentials...")
    env_vars = load_env_variables(args.env_file)
    
    # Step 1: Create batch files
    logging.info("Creating batch files...")
    processor = MultimodalBatchProcessor(
        dataset_path=args.dataset,
        prompt_file=args.prompt,
        output_dir=args.output_dir
    )
    processor.create_batches(env_vars['deployment_name'])
    
    # Step 2: Submit batches
    logging.info("Submitting batches to Azure OpenAI...")
    batch_manager = AzureBatchManager(
        api_key=env_vars['api_key'],
        api_endpoint=env_vars['api_endpoint'],
        api_version=env_vars['api_version'],
        deployment_name=env_vars['deployment_name'],
        batch_tracking_file=args.tracking_file
    )
    batch_manager.submit_all_batches(args.output_dir)
    
    logging.info("✓ Batch submission complete!")
    logging.info(f"  Batch files: {args.output_dir}")
    logging.info(f"  Tracking file: {args.tracking_file}")
    logging.info("\nNext step: Wait for batches to complete (up to 24 hours)")
    logging.info(f"Then run: python 2_retrieve_results.py --env_file {args.env_file} --tracking_file {args.tracking_file}")


if __name__ == "__main__":
    main()
