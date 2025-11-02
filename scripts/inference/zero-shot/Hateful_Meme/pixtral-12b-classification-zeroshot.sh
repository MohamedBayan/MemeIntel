#!/bin/bash

#export MAX_PIXELS=1003520 

swift infer \
    --model mistral-community/pixtral-12b \
    --infer_backend pt \
    --val_dataset ./data/ms_swift_formated/Hateful/classification/test.jsonl \
    --gpu_memory_utilization 0.95 \
    --max_new_tokens 512 \
    --use_hf true \
    --max_batch_size 1 \
    --temperature 0 \
    --result_path ./result/zero-shot/Hateful_Meme/pixtral-12b-classification-zeroshot.jsonl \
