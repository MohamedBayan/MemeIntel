#!/bin/bash
# Retrieve and merge results for ArMeme English explanations

# Configuration
DATASET="/path/to/your/armeme_dataset.jsonl"
ENV_FILE="/path/to/your/.env"
OUTPUT_BASE="/path/to/output/directory"

echo "================================================"
echo "ArMeme English Explanation - Retrieve & Merge"
echo "================================================"

# Step 2: Retrieve results
echo ""
echo "Step 2: Retrieving batch results..."
python 2_retrieve_results.py \
    --env_file "$ENV_FILE" \
    --tracking_file "$OUTPUT_BASE/tracking/batch_tracking_armeme_en.txt" \
    --output_dir "$OUTPUT_BASE/results_en"

if [ $? -ne 0 ]; then
    echo "Error: Result retrieval failed!"
    exit 1
fi

# Step 3: Merge explanations
echo ""
echo "Step 3: Merging explanations with dataset..."
python 3_merge_results_explanation.py \
    --dataset "$DATASET" \
    --results_dir "$OUTPUT_BASE/results_en" \
    --output "$OUTPUT_BASE/armeme_with_english_explanations.jsonl"

if [ $? -ne 0 ]; then
    echo "Error: Merge failed!"
    exit 1
fi

echo ""
echo "✓ Complete! Dataset with English explanations saved to:"
echo "  $OUTPUT_BASE/armeme_with_english_explanations.jsonl"
