#!/bin/bash
# Retrieve and merge results for Hateful Memes explanations

# Configuration
DATASET="/path/to/your/hateful_memes_dataset.jsonl"
ENV_FILE="/path/to/your/.env"
OUTPUT_BASE="/path/to/output/directory"

echo "================================================"
echo "Hateful Memes Explanation - Retrieve & Merge"
echo "================================================"

# Step 2: Retrieve results
echo ""
echo "Step 2: Retrieving batch results..."
python 2_retrieve_results.py \
    --env_file "$ENV_FILE" \
    --tracking_file "$OUTPUT_BASE/tracking/batch_tracking_hateful.txt" \
    --output_dir "$OUTPUT_BASE/results"

if [ $? -ne 0 ]; then
    echo "Error: Result retrieval failed!"
    exit 1
fi

# Step 3: Merge explanations
echo ""
echo "Step 3: Merging explanations with dataset..."
python 3_merge_results_explanation.py \
    --dataset "$DATASET" \
    --results_dir "$OUTPUT_BASE/results" \
    --output "$OUTPUT_BASE/hateful_memes_with_explanations.jsonl"

if [ $? -ne 0 ]; then
    echo "Error: Merge failed!"
    exit 1
fi

echo ""
echo "✓ Complete! Dataset with explanations saved to:"
echo "  $OUTPUT_BASE/hateful_memes_with_explanations.jsonl"
