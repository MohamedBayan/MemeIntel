#!/bin/bash



swift infer \
    --model meta-llama/Llama-3.2-11B-Vision-Instruct \
    --infer_backend pt \
    --val_dataset ./data/ms_swift_formated/Hateful/explanation/test.jsonl \
    --gpu_memory_utilization 0.95 \
    --max_new_tokens 2048 \
    --use_hf true \
    --max_batch_size 8 \
    --temperature 0 \
    --result_path ./result/zero-shot/Hateful_Meme/Llama-3.2-11B-explanation-zeroshot.jsonl \
