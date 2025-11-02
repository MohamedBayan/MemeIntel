#!/bin/bash

# export NPROC_PER_NODE=8
# export CUDA_VISIBLE_DEVICES=0,1,1,2,3,4,5,6,7


swift infer \
    --model meta-llama/Llama-3.2-11B-Vision-Instruct \
    --infer_backend pt \
    --val_dataset ./data/ms_swift_formated/ArMeme/explanation/explanation_en/test.jsonl \
    --gpu_memory_utilization 0.95 \
    --max_new_tokens 2048 \
    --use_hf true \
    --temperature 0 \
    --result_path ./result/zero-shot/ArMeme/Llama-3.2-11B-explanation_en-zeroshot.jsonl \
