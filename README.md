# [MemeIntel: Explainable Detection of Propagandistic and Hateful Memes](https://arxiv.org/abs/2502.16612)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![Paper](https://img.shields.io/badge/Paper-arXiv-red.svg)](https://arxiv.org/abs/2502.16612)

## Overview

This repository contains the official implementation for **MemeIntel**, a framework for explainable detection of propagandistic and hateful memes. The system performs both classification and explanation generation for multimodal content.

![Experimental Pipeline](assets/Figure_1.png)
*Figure 1: Experimental pipeline for explanation generation and training.*

## Features

- 🎯 **Classification & Explanation**: Detects propaganda/hate and generates detailed explanations
- 🔧 **Multiple Training Strategies**: Single-task, multi-task, and multi-stage training
- 🌐 **Multilingual Support**: Arabic and English datasets and explanations
- 🤖 **Modern Vision-Language Models**: Llama-3.2-Vision, Qwen2-VL, PaliGemma2, Pixtral

## Supported Models

| Model | Size | Tasks |
|-------|------|-------|
| **Llama-3.2-Vision** | 11B | Classification, Explanation |
| **Qwen2-VL** | 7B | Classification, Explanation |
| **PaliGemma2** | 3B | Classification, Explanation |
| **Pixtral** | 12B | Classification, Explanation |

## Datasets

### ArMeme_Xplain (Arabic Propagandistic Memes)
- **Location**: `data/ArMeme_Xplain/`
- **Language**: Arabic text with Arabic/English explanations
- **Labels**: `propaganda`, `not-propaganda`, `not-meme`, `other`
- **Format**: JSONL with images

### Hateful_memes_Xplain (English Hateful Memes)
- **Location**: `data/hateful_memes_Xplain/`
- **Language**: English
- **Labels**: `hateful`, `non-hateful`
- **Format**: JSONL with images

Both datasets include multimodal content (image + text) with human-annotated explanations.

## Installation

```bash
# Create and activate environment
conda create -n MemeIntel python=3.10 -y
conda activate MemeIntel

# Install MS-Swift framework
pip install 'ms-swift[all]' -U

# Install evaluation dependencies
pip install bert-score rouge-score nltk evaluate scikit-learn matplotlib seaborn pandas

# Clone repository
git clone https://github.com/MohamedBayan/MemeIntel.git
cd MemeIntel
```

## Data Preparation

The datasets need to be converted to MS-Swift format before training:

```bash
# Convert ArMeme dataset
bash scripts/run_armeme_format.sh

# Convert Hateful Memes dataset
bash scripts/run_hateful_format.sh
```

This creates formatted data in `data/ms_swift_formated/` with separate directories for classification and explanation tasks.

## Generating Explanations

We provide scripts to generate explanations using Azure OpenAI Batch API in `scripts/batch_infer/`:

```bash
cd scripts/batch_infer

# Submit batch job for explanation generation
python 1_submit_batches.py \
    --dataset /path/to/dataset.jsonl \
    --prompt prompts/armeme_explanation_arabic.txt \
    --env_file .env \
    --output_dir ./batches

# Retrieve results
python 2_retrieve_results.py --tracking_file batch_tracking.txt

# Merge explanations back to dataset
python 3_merge_results_explanation.py \
    --original dataset.jsonl \
    --explanations results.jsonl \
    --output final_with_explanations.jsonl
```

See `scripts/batch_infer/README.md` for detailed documentation.

## Training

### Single-Stage Training (Classification or Explanation)

```bash
# ArMeme - Classification
bash scripts/train/ArMeme/llama-3.2-11b-classification-ss-lora.sh
bash scripts/train/ArMeme/qwen2-vl-7b-classification-ss-lora.sh

# ArMeme - Arabic Explanation
bash scripts/train/ArMeme/llama-3.2-11b-explanation_ar-ss-lora.sh

# Hateful Memes - Classification
bash scripts/train/Hateful_Meme/llama-3.2-11b-classification-ss-lora.sh

# Hateful Memes - Explanation
bash scripts/train/Hateful_Meme/llama-3.2-11b-explanation-ss-lora.sh
```

### Multi-Stage Training

```bash
# Stage 2: Fine-tune on Hateful Memes explanations
bash scripts/train/Hateful_Meme/llama-3.2-11b-explanation-ms-lora.sh
```

## Inference

### Zero-Shot Evaluation

```bash
# Classification
bash scripts/inference/zero-shot/ArMeme/llama-3.2-11b-classification-zeroshot.sh

# Explanation generation
bash scripts/inference/zero-shot/ArMeme/llama-3.2-11b-explanation_ar-zeroshot.sh
```

### Fine-Tuned Model Evaluation

```bash
bash scripts/inference/fine-tuned/ArMeme/llama-3.2-11b-classification-finetuned.sh
bash scripts/inference/fine-tuned/Hateful_Meme/qwen2-vl-7b-explanation-finetuned.sh
```

## Evaluation

Evaluate predictions and compute metrics:

```bash
bash scripts/evaluate.sh
```

This script computes classification metrics (F1, precision, recall) and explanation quality metrics (BERTScore, ROUGE).

## Repository Structure

```
MemeIntel/
├── data/                                # Datasets
│   ├── ArMeme_Xplain/                  # Raw ArMeme dataset
│   ├── hateful_memes_Xplain/           # Raw Hateful Memes dataset
│   └── ms_swift_formated/              # Formatted for training
│       ├── ArMeme/
│       │   ├── classification/
│       │   └── explanation/
│       │       ├── explanation_ar/
│       │       └── explanation_en/
│       └── Hateful/
│           ├── classification/
│           └── explanation/
├── scripts/
│   ├── batch_infer/                    # Azure OpenAI explanation generation
│   │   ├── 1_submit_batches.py
│   │   ├── 2_retrieve_results.py
│   │   ├── 3_merge_results_explanation.py
│   │   └── README.md
│   ├── train/                          # Training scripts
│   │   ├── ArMeme/                     # ArMeme training scripts
│   │   └── Hateful_Meme/               # Hateful Meme training scripts
│   ├── inference/                      # Inference scripts
│   │   ├── zero-shot/
│   │   └── fine-tuned/
│   ├── src/
│   │   └── compute_metrics.py          # Evaluation metrics
│   ├── run_armeme_format.sh            # Data formatting
│   ├── run_hateful_format.sh
│   └── evaluate.sh                     # Batch evaluation
├── result/                             # Inference outputs
├── scores/                             # Evaluation results
└── README.md
```

## Dataset Format

### Raw Format (before conversion)

**ArMeme_Xplain:**
```json
{
    "id": "unique_id",
    "text": "Arabic text from meme",
    "img_path": "./data/arabic_memes_fb_insta_pinterest/...",
    "class_label": "propaganda",
    "explanation_en": "English explanation",
    "explanation_ar": "Arabic explanation"
}
```

**hateful_memes_Xplain:**
```json
{
    "id": 12345,
    "text": "English text from meme",
    "img_path": "img/12345.png",
    "class_label": "non-hateful",
    "explanation": "Explanation of classification"
}
```

### MS-Swift Format (after conversion)

After running the formatting scripts, data is converted to MS-Swift format:

**Classification:**
```json
{
    "messages": [
        {"role": "system", "content": "System prompt..."},
        {"role": "user", "content": "Task...<image> Text: [text]"},
        {"role": "assistant", "content": "Label: propaganda"}
    ],
    "images": ["./data/ArMeme_Xplain/data/..."]
}
```

**Explanation:**
```json
{
    "messages": [
        {"role": "system", "content": "System prompt..."},
        {"role": "user", "content": "Task...<image> Text: [text]"},
        {"role": "assistant", "content": "Label: propaganda\nExplanation: [explanation]"}
    ],
    "images": ["./data/ArMeme_Xplain/data/..."]
}
```

## Citation

If you use our resources, please cite:

```bibtex
@misc{kmainasi2025memeintelexplainabledetectionpropagandistic,
      title={MemeIntel: Explainable Detection of Propagandistic and Hateful Memes}, 
      author={Mohamed Bayan Kmainasi and Abul Hasnat and Md Arid Hasan and Ali Ezzat Shahroor and Firoj Alam},
      year={2025},
      eprint={2502.16612},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2502.16612}, 
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MS-Swift](https://github.com/modelscope/ms-swift) - Training framework
