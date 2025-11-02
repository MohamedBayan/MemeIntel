#!/bin/bash

export TORCH_COMPILE_DISABLE=1


swift infer \
    --model google/paligemma2-3b-pt-224 \
    --infer_backend pt \
    --val_dataset ./data/ms_swift_formated/Hateful/explanation/test.jsonl \
    --gpu_memory_utilization 0.95 \
    --max_new_tokens 2048 \
    --use_hf true \
    --max_batch_size 8 \
    --temperature 0 \
    --result_path ./result/zero-shot/Hateful_Meme/paligemma2-3b-explanation-zeroshot.jsonl \
