# python scripts/src/compute_metrics.py \
#   --data result/fine-tuned/ArMeme/gemma-3-12b-classification-zeroshot.jsonl \
#   --out_dir scores


# python scripts/src/compute_metrics.py \
#   --data result/fine-tuned/ArMeme/gemma-3-12b-it-explanation_ar-ss-lora.jsonl \
#   --out_dir scores \
#     --has_explanation \
#     --is_arabic


DATA_DIR="./result/zero-shot/Hateful_Meme"
OUT_DIR="./scores/zero-shot/Hateful_Meme"
SCRIPT="./scripts/src/compute_metrics.py"

for file in "$DATA_DIR"/*.jsonl; do
    echo "Processing $file ..."
    base=$(basename "$file" .jsonl)

    # Check conditions for extra args
    ARGS=""
    if [[ "$file" == *"explanation"* ]]; then
        ARGS="$ARGS --has_explanation"
    fi
    if [[ "$file" == *"_ar"* ]]; then
        ARGS="$ARGS --is_arabic"
    fi

    # Run the command
    python "$SCRIPT" \
        --data "$file" \
        --out_dir "$OUT_DIR/$base" \
        $ARGS

    echo "Done with $file"
done
