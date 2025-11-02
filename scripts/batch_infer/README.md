# Batch Inference for Explanation Generation# Batch Inference Scripts - Explanation Generation



Batch inference system for generating explanations for classified meme datasets using Azure OpenAI Batch API.Batch inference system for generating explanations for multimodal meme datasets using Azure OpenAI Batch API.



## Overview## Purpose



This system generates explanations for already-classified memes. It does NOT perform classification - it explains why a human expert classified the image as they did.This system generates explanations for **already-classified** memes by analyzing visual elements, text content, and their interaction. It does NOT perform classification - it explains why a human expert classified the image as they did.



The system:## Quick Start

1. Takes your dataset with class_label

2. Substitutes the label into the prompt (replaces {} placeholder)### 1. Prepare Your Data

3. Sends image + customized prompt to Azure OpenAI

4. Parses the JSON response containing the explanation**Dataset Format** (`dataset.jsonl`):

5. Adds explanation field to your original dataset```json

{"id": "unique_id", "img_path": "/path/to/image1.jpg", "class_label": "propaganda", "text": "مصر أولاً"}

## Dataset Format{"id": "unique_id2", "img_path": "/path/to/image2.jpg", "class_label": "not-propaganda", "text": "Life is good"}

```

### Input (example_dataset.jsonl)

**Required fields:**

```json- `id`: Unique identifier for each item

{- `img_path`: Absolute path to the image file

  "id": "data/arabic_memes_fb_insta_pinterest/Instagram/IMAGES/ex.officiall/2020-02-27_14-10-48_UTC.jpg",- `class_label`: The human-classified label (e.g., "propaganda", "not-propaganda", "hateful", "not-hateful")

  "text": "اااااه\n\n*الدفعات القديمة*\n\nلو نقصت ٤٠ درجة هجيب 90%\nده مين المتخلف إللي ينقص ٤٠ درجة؟!\n",

  "img_path": "/alt/vllms/mohamedbayan/MemeReason/data/ArMeme_Think/data/arabic_memes_fb_insta_pinterest/Instagram/IMAGES/ex.officiall/2020-02-27_14-10-48_UTC.jpg",**Optional fields:**

  "class_label": "propaganda"- `text`: Extracted text from the meme

}

```**Prompt Files** (already created in `prompts/`):

- `armeme_explanation_arabic.txt` - Arabic explanations for ArMeme (100 words)

Required fields:- `armeme_explanation_english.txt` - English explanations for ArMeme (100 words)

- `id`: Unique identifier for each item- `hateful_memes_explanation.txt` - English explanations for Hateful Memes (100 words)

- `img_path`: Absolute path to the image file

- `class_label`: The human-classified label (e.g., "propaganda", "not-propaganda", "hateful", "not-hateful")**Environment File** (`.env`):

```bash

Optional fields:AZURE_API_KEY=your-api-key

- `text`: Extracted text from the memeAZURE_API_URL=https://your-resource.openai.azure.com

AZURE_API_VERSION=2024-02-15-preview

### Output (example_output_with_explanations.jsonl)AZURE_ENGINE_NAME=gpt-4o

```

```json

{### 2. Run the Pipeline

  "id": "data/arabic_memes_fb_insta_pinterest/Instagram/IMAGES/ex.officiall/2020-02-27_14-10-48_UTC.jpg",

  "text": "اااااه\n\n*الدفعات القديمة*\n\nلو نقصت ٤٠ درجة هجيب 90%\nده مين المتخلف إللي ينقص ٤٠ درجة؟!\n",**Step 1: Submit Batches**

  "img_path": "/alt/vllms/mohamedbayan/MemeReason/data/ArMeme_Think/data/arabic_memes_fb_insta_pinterest/Instagram/IMAGES/ex.officiall/2020-02-27_14-10-48_UTC.jpg",```bash

  "class_label": "propaganda",python 1_submit_batches.py \

  "explanation": "The image uses humor and exaggeration to mock older generations ('الدفعات القديمة') by implying their academic standards were so lenient that even losing 40 marks would still result in a high score of 90%. The text is sarcastic, calling the person who deducts 40 marks 'mentally challenged' ('مين المتخلف'). The visual elements, including casual clothing and a TV interview setting, reinforce the informal and relatable tone. The laughing emojis amplify the humor and emotional appeal, encouraging viewers to align with the critique. This combination of humor and ridicule is a classic propaganda technique to influence opinions on generational differences."    --dataset /path/to/dataset.jsonl \

}    --prompt prompts/armeme_explanation_arabic.txt \

```    --env_file .env \

    --output_dir ./batches \

## Prompts    --tracking_file ./batch_tracking.txt

```

Three prompts are available in `prompts/`:

**Step 2: Retrieve Results** (after 1-24 hours)

1. `armeme_explanation_arabic.txt` - Arabic explanations for ArMeme (100 words)```bash

2. `armeme_explanation_english.txt` - English explanations for ArMeme (100 words)python 2_retrieve_results.py \

3. `hateful_memes_explanation.txt` - English explanations for Hateful Memes (100 words)    --env_file .env \

    --tracking_file ./batch_tracking.txt \

Each prompt:    --output_dir ./results

- Uses {} placeholder for class_label substitution```

- Instructs the model NOT to re-classify (analysis only)

- Requests JSON output: {"explanation": "..."}**Step 3: Merge Explanations**

- Limited to 100 words```bash

python 3_merge_results_explanation.py \

## Environment Setup    --dataset /path/to/dataset.jsonl \

    --results_dir ./results \

Create a `.env` file with your Azure OpenAI credentials:    --output ./dataset_with_explanations.jsonl

```

```bash

AZURE_API_KEY=your-api-key-here## Output Format

AZURE_API_URL=https://your-resource.openai.azure.com

AZURE_API_VERSION=2024-02-15-previewThe final output adds a `generated_explanation` field to each item:

AZURE_ENGINE_NAME=gpt-4o

``````json

{

## Usage  "id": "armeme_001",

  "img_path": "/path/to/image1.jpg",

### Step 1: Submit Batches  "class_label": "propaganda",

  "text": "مصر أولاً",

```bash  "generated_explanation": "الصورة تعرض علمًا مصريًا... (Arabic explanation)"

python 1_submit_batches.py \}

    --dataset /path/to/dataset.jsonl \```

    --prompt prompts/armeme_explanation_arabic.txt \

    --env_file .env \See `example_output_with_explanations.jsonl` for complete examples.

    --output_dir ./batches \

    --tracking_file ./batch_tracking.txt## How It Works

```

The system:

This creates batch files and submits them to Azure OpenAI.1. Takes your dataset with `class_label` 

2. Substitutes the label into the prompt (replaces `{}` placeholder)

### Step 2: Retrieve Results3. Sends image + customized prompt to Azure OpenAI

4. Parses the JSON response containing the explanation

Wait 1-24 hours for processing, then:5. Adds `generated_explanation` field to your original dataset



```bash## Features

python 2_retrieve_results.py \

    --env_file .env \- ✓ Simple 3-step process

    --tracking_file ./batch_tracking.txt \- ✓ Automatic class_label substitution in prompts

    --output_dir ./results- ✓ Automatic batch file creation (respects 180MB limit)

```- ✓ Handles large images (up to 10MB each)

- ✓ Base64 image encoding

This downloads completed batch results.- ✓ Robust JSON parsing with fallback

- ✓ Preserves all original dataset fields

### Step 3: Merge Explanations- ✓ Progress tracking

- ✓ Error handling

```bash- ✓ Arabic text support

python 3_merge_results_explanation.py \

    --dataset /path/to/dataset.jsonl \## File Structure

    --results_dir ./results \

    --output ./dataset_with_explanations.jsonl```

```batch_infer/

├── batch_processor.py                    # Core library (with class_label substitution)

This adds the explanation field to your original dataset.├── 1_submit_batches.py                   # Step 1: Submit

├── 2_retrieve_results.py                 # Step 2: Retrieve

## Example Shell Scripts├── 3_merge_results_explanation.py        # Step 3: Merge explanations

├── prompts/                              # Prompt templates

Pre-configured scripts are available in `scripts/`:│   ├── armeme_explanation_arabic.txt     # ArMeme Arabic (100 words)

│   ├── armeme_explanation_english.txt    # ArMeme English (100 words)

**ArMeme Arabic:**│   └── hateful_memes_explanation.txt     # Hateful Memes (100 words)

```bash├── scripts/                              # Example shell scripts

bash scripts/armeme_arabic_explanation_submit.sh│   ├── armeme_arabic_explanation_submit.sh

# Wait 1-24 hours│   ├── armeme_arabic_explanation_retrieve.sh

bash scripts/armeme_arabic_explanation_retrieve.sh│   ├── armeme_english_explanation_submit.sh

```│   ├── armeme_english_explanation_retrieve.sh

│   ├── hateful_memes_explanation_submit.sh

**ArMeme English:**│   └── hateful_memes_explanation_retrieve.sh

```bash├── example_dataset.jsonl                 # Example input

bash scripts/armeme_english_explanation_submit.sh├── example_output_with_explanations.jsonl # Example output

# Wait 1-24 hours├── README.md                             # This file

bash scripts/armeme_english_explanation_retrieve.sh├── SETUP_SUMMARY.md                      # Complete setup guide

```├── EXPLANATION_GENERATION_README.md      # Detailed documentation

├── PROMPT_SPECIFICATIONS.md              # Prompt details

**Hateful Memes:**└── VERIFICATION_CHECKLIST.md             # Pre-flight checklist

```bash```

bash scripts/hateful_memes_explanation_submit.sh

# Wait 1-24 hoursWorking directory after running:

bash scripts/hateful_memes_explanation_retrieve.sh```

```├── batches/                    # Generated batch files

│   ├── batch_1.jsonl

Note: Update the paths in these scripts before using them.│   └── batch_2.jsonl

├── results/                    # Retrieved results

## File Structure│   ├── batch_output_xxx.jsonl

│   └── batch_output_yyy.jsonl

```├── batch_tracking.txt          # Batch ID tracking

batch_infer/└── dataset_with_explanations.jsonl  # Final dataset with explanations

├── batch_processor.py                    # Core library (with class_label substitution)```

├── 1_submit_batches.py                   # Step 1: Submit

├── 2_retrieve_results.py                 # Step 2: Retrieve## Important Notes

├── 3_merge_results_explanation.py        # Step 3: Merge explanations

├── prompts/                              # Prompt templates- **No Re-classification**: Prompts instruct the model NOT to re-classify images

│   ├── armeme_explanation_arabic.txt- **Class Label Substitution**: The `{}` in prompts is automatically replaced with `class_label`

│   ├── armeme_explanation_english.txt- **100 Word Limit**: All prompts request ~100 word explanations

│   └── hateful_memes_explanation.txt- **JSON Output**: Explanations are returned as JSON and automatically parsed

├── scripts/                              # Example shell scripts- **ID Matching**: Uses `id` field to match results with original data

│   ├── armeme_arabic_explanation_submit.sh

│   ├── armeme_arabic_explanation_retrieve.sh## Tips

│   ├── armeme_english_explanation_submit.sh

│   ├── armeme_english_explanation_retrieve.sh1. **Test First**: Try with a small subset (10-20 items) to verify everything works

│   ├── hateful_memes_explanation_submit.sh2. **Check Status**: You can run step 2 multiple times to check if batches are ready

│   └── hateful_memes_explanation_retrieve.sh3. **Cost**: Batch API is 50% cheaper than standard API but takes longer

├── example_dataset.jsonl                 # Example input4. **Keep Tracking File**: Don't delete `batch_tracking.txt` - you need it to retrieve results!

├── example_output_with_explanations.jsonl # Example output5. **Use Example Scripts**: Pre-configured shell scripts are in `scripts/` directory

└── README.md                             # This file

```## Requirements



## FeaturesInstall dependencies:

```bash

- Simple 3-step processpip install openai python-dotenv

- Automatic class_label substitution in prompts```

- Automatic batch file creation (respects 180MB limit)

- Handles large images (up to 10MB each)## Documentation

- Base64 image encoding

- Robust JSON parsing with fallback- **Quick Start**: This README

- Preserves all original dataset fields- **Complete Guide**: `SETUP_SUMMARY.md`

- Progress tracking- **Detailed Usage**: `EXPLANATION_GENERATION_README.md`

- Error handling- **Prompt Details**: `PROMPT_SPECIFICATIONS.md`

- Arabic text support- **Checklist**: `VERIFICATION_CHECKLIST.md`



## Requirements## Troubleshooting



Install dependencies:**"Image not found" errors**: 

- Verify `img_path` uses absolute paths

```bash- Ensure all image files exist

pip install openai python-dotenv

```**"No completed batches found"**:

- Wait longer - batch jobs can take up to 24 hours

## Important Notes- Check Azure portal for batch status



- **No Re-classification**: Prompts instruct the model NOT to re-classify images**Missing explanations in output**:

- **Class Label Substitution**: The {} in prompts is automatically replaced with class_label- Some batches may still be processing

- **100 Word Limit**: All prompts request approximately 100 word explanations- Re-run step 2 and 3 after waiting longer

- **JSON Output**: Explanations are returned as JSON and automatically parsed- Check for `null` values in `generated_explanation` field

- **ID Matching**: Uses id field to match results with original data

- **Image Paths**: Must be absolute paths**JSON parsing errors**:

- **Batch Processing Time**: 1-24 hours- The merge script handles common issues automatically

- Check raw result files if needed

## Troubleshooting

## Example Usage

**"Image not found" errors**

- Verify img_path uses absolute pathsSee `example_dataset.jsonl` for input format and `example_output_with_explanations.jsonl` for expected output.

- Ensure all image files exist

For complete examples with actual datasets, see the shell scripts in `scripts/` directory.

**"No completed batches found"**

- Wait longer - batch jobs can take up to 24 hours## Support

- Check Azure portal for batch status

For detailed setup and troubleshooting, refer to:

**Missing explanations in output**- `SETUP_SUMMARY.md` - Complete overview

- Some batches may still be processing- `VERIFICATION_CHECKLIST.md` - Pre-flight checklist

- Re-run step 2 and 3 after waiting longer
- Check for null values in explanation field

**JSON parsing errors**
- The merge script handles common issues automatically
- Check raw result files if needed

## Tips

1. Test with a small subset (10-20 items) first
2. Check batch status by running step 2 multiple times
3. Batch API is 50% cheaper than standard API but takes longer
4. Keep the tracking file - you need it to retrieve results
5. Use example scripts as templates for your datasets
