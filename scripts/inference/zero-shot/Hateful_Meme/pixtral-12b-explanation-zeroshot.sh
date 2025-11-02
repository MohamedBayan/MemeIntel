#!/bin/bash
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export NPROC_PER_NODE=8

swift infer \
    --model mistral-community/pixtral-12b \
    --infer_backend pt \
    --val_dataset ./data/ms_swift_formated/Hateful/explanation/test.jsonl \
    --gpu_memory_utilization 0.95 \
    --max_new_tokens 2048 \
    --use_hf true \
    --max_batch_size 1 \
    --temperature 0 \
    --result_path ./result/zero-shot/Hateful_Meme/pixtral-12b-explanation-zeroshot.jsonl \