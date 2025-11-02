#!/bin/bash



swift infer \
    --model mistral-community/pixtral-12b \
    --infer_backend pt \
    --val_dataset ./data/ms_swift_formated/ArMeme/explanation/explanation_ar/test.jsonl \
    --gpu_memory_utilization 0.95 \
    --max_new_tokens 2048 \
    --use_hf true \
    --temperature 0 \
    --result_path ./result/zero-shot/ArMeme/pixtral-12b-explanation_ar-zeroshot.jsonl \
