#!/bin/bash

swift infer \
    --infer_backend pt \
    --val_dataset ./data/ms_swift_formated/Hateful/classification/test.jsonl \
    --adapters ./training_checkpoints/Hateful_Meme/llama-3.2-11b-classification-ss-lora/v*-*-*/checkpoint-best \
    --gpu_memory_utilization 0.95 \
    --max_new_tokens 2048 \
    --use_hf true \
    --result_path ./result/fine-tuned/Hateful_Meme/llama-3.2-11b-classification-ss-lora.jsonl