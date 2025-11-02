#!/bin/bash


export TORCH_COMPILE_DISABLE=1

swift infer \
    --model google/paligemma2-3b-pt-224 \
    --infer_backend pt \
    --val_dataset ./data/ms_swift_formated/ArMeme/explanation/explanation_ar/test.jsonl \
    --gpu_memory_utilization 0.95 \
    --max_new_tokens 2048 \
    --use_hf true \
    --max_batch_size 4 \
    --temperature 0 \
    --result_path  ./result/zero-shot/ArMeme/paligemma2-3b-explanation_ar-zeroshot.jsonl \