#!/bin/bash

swift infer \
    --infer_backend pt \
    --val_dataset "./data/ms_swift_formated/ArMeme/explanation/explanation_en/test.jsonl" \
    --adapters ./training_checkpoints/ArMeme/llama-3.2-11b-explanation_en-ss-lora/v*-*-*/checkpoint-best \
    --gpu_memory_utilization 0.95
    --max_new_tokens 2048 \
    --use_hf true \
    --max_batch_size 16 \
    --result_path ./result/fine-tuned/ArMeme/llama-3.2-11b-explanation_en-ss-lora.jsonl