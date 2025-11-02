#!/bin/bash
# Example workflow for generating explanations for Hateful Memes dataset

# Configuration
DATASET="/path/to/your/hateful_memes_dataset.jsonl"
PROMPT="/alt/vllms/mohamedbayan/batch_infer/prompts/hateful_memes_explanation.txt"
ENV_FILE="/path/to/your/.env"
OUTPUT_BASE="/path/to/output/directory"

# Create output directories
mkdir -p "$OUTPUT_BASE/batches"
mkdir -p "$OUTPUT_BASE/results"
mkdir -p "$OUTPUT_BASE/tracking"

echo "================================================"
echo "Hateful Memes Explanation Generation"
echo "================================================"

# Step 1: Submit batches
echo ""
echo "Step 1: Submitting batches..."
python 1_submit_batches.py \
    --dataset "$DATASET" \
    --prompt "$PROMPT" \
    --env_file "$ENV_FILE" \
    --output_dir "$OUTPUT_BASE/batches" \
    --tracking_file "$OUTPUT_BASE/tracking/batch_tracking_hateful.txt"

if [ $? -ne 0 ]; then
    echo "Error: Batch submission failed!"
    exit 1
fi

echo ""
echo "✓ Batches submitted successfully!"
echo "Wait 1-24 hours for processing, then run the retrieve step."
echo ""
echo "To retrieve results later, run:"
echo "bash scripts/hateful_memes_explanation_retrieve.sh"
