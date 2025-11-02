#!/bin/bash

python scripts/src/format_dataset.py \
  --data_base_path ./data/hateful_memes_Xplain \
  --output_dir ./data/ms_swift_formated/Hateful \
  --dataset_type hateful
