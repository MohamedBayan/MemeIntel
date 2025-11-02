#!/bin/bash



swift infer \
    --model Qwen/Qwen2-VL-7B-Instruct \
    --infer_backend pt \
    --val_dataset ./data/ms_swift_formated/ArMeme/explanation/explanation_en/test.jsonl \
    --gpu_memory_utilization 0.95 \
    --max_new_tokens 2048 \
    --use_hf true \
    --temperature 0 \
    --result_path ./result/zero-shot/ArMeme/Qwen2-VL-7B-explanation_en-zeroshot.jsonl \
