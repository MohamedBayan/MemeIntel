CUDA_VISIBLE_DEVICES=0 \
swift export \
    --adapters ./training_checkpoints/ArMeme/llama-3.2-11b-explanation_en-ss-lora/<vx-xxx>/checkpoint-xxx \
    --merge_lora true \
    --output_dir ./models/vx-xxx/merged_model_ArMeme_en_stage1 \