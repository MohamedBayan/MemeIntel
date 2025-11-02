#!/bin/bash
# Retrieve and merge results for ArMeme Arabic explanations

# Configuration
DATASET="/path/to/your/armeme_dataset.jsonl"
ENV_FILE="/path/to/your/.env"
OUTPUT_BASE="/path/to/output/directory"

echo "================================================"
echo "ArMeme Arabic Explanation - Retrieve & Merge"
echo "================================================"

# Step 2: Retrieve results
echo ""
echo "Step 2: Retrieving batch results..."
python 2_retrieve_results.py \
    --env_file "$ENV_FILE" \
    --tracking_file "$OUTPUT_BASE/tracking/batch_tracking_armeme_ar.txt" \
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
    --output "$OUTPUT_BASE/armeme_with_arabic_explanations.jsonl"

if [ $? -ne 0 ]; then
    echo "Error: Merge failed!"
    exit 1
fi

echo ""
echo "✓ Complete! Dataset with Arabic explanations saved to:"
echo "  $OUTPUT_BASE/armeme_with_arabic_explanations.jsonl"
