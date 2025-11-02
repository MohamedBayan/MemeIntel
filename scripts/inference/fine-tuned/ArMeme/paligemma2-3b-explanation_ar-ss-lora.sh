#!/bin/bash

export nproc_per_node=8
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export TORCH_COMPILE_DISABLE=1


swift infer \
    --infer_backend pt \
    --val_dataset "./data/ms_swift_formated/ArMeme/explanation/explanation_ar/test.jsonl" \
    --adapters ./training_checkpoints/ArMeme/paligemma2-3b-explanation_ar-ss-lora/v*-*-*/checkpoint-best \
    --gpu_memory_utilization 0.95 \
    --max_new_tokens 2048 \
    --use_hf true \
    --max_batch_size 16 \
    --result_path ./result/fine-tuned/ArMeme/paligemma2-3b-explanation_ar-ss-lora.jsonl \

