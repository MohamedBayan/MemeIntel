#!/bin/bash

export NPROC_PER_NODE=8
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export TORCH_COMPILE_DISABLE=1


swift infer \
    --model google/paligemma2-3b-pt-224 \
    --infer_backend pt \
    --val_dataset ./data/ms_swift_formated/ArMeme/classification/test.jsonl \
    --gpu_memory_utilization 0.95 \
    --max_new_tokens 2048 \
    --use_hf true \
    --temperature 0 \
    --result_path ./result/zero-shot/ArMeme/paligemma2-3b-classification-zeroshot.jsonl \
