# format_dataset.py
import argparse
import os
import json
import pandas as pd
from typing import List, Dict

def format_data(
    df: pd.DataFrame,
    instruction: str,
    system_prompt: str,
    task_type: str,
    data_base_path: str,
    text_column: str = 'text',
    image_column: str = 'img_path',
    class_column: str = 'class_label',
    explanation_column: str = 'explanation'
) -> List[Dict]:
    formatted_data = []
    for _, row in df.iterrows():
        label = row.get(class_column, "N/A")
        explanation = row.get(explanation_column, "")
        text = row.get(text_column, "")
        image_filename = row.get(image_column, "")
        if image_filename.startswith("."):
            image_filename = image_filename[2:]
        image_path = os.path.join(data_base_path, image_filename)

        if task_type == "classification":
            output = f"Label: {label}"
        else:
            output = f"Label: {label}\nExplanation: {explanation}"

        entry = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{instruction}<image> Text extracted: {text}"},
                {"role": "assistant", "content": output}
            ],
            "images": [image_path],
        }
        formatted_data.append(entry)
    return formatted_data

def save_jsonl(data: List[Dict], save_path: str):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w', encoding='utf-8') as f:
        for entry in data:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')

def load_datasets(data_base_path: str, suffixes: List[str]) -> Dict[str, pd.DataFrame]:
    return {
        split: pd.read_json(os.path.join(data_base_path, f"{split}{suffix}.jsonl"), lines=True)
        for split, suffix in zip(["train", "test", "dev"], suffixes)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_base_path", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--dataset_type", type=str, choices=["armeme", "hateful"], required=True)

    args = parser.parse_args()
    suffixes = {
        "armeme": ["", "", ""],
        "hateful": ["", "", ""]
    }[args.dataset_type]

    dataset = load_datasets(args.data_base_path, suffixes)

    if args.dataset_type == "armeme":
        SYS_PROMPT = "You are an expert social media image analyzer specializing in identifying propaganda in Arabic contexts."
        INSTRUCTION_CLS = (
            "You are an expert social media image analyzer specializing in identifying propaganda in Arabic contexts. "
            "I will provide you with Arabic memes and the text extracted from these images. Your task is to classify the image as one of the following: "
            "'propaganda', 'not-propaganda', 'not-meme', or 'other'. Return only the label, and start your response with 'Label:' followed by the classification label."
        )
        INSTRUCTIONS_EXP = {
            "explanation_ar": (
                "You are an expert social media image analyzer specializing in identifying propaganda in Arabic contexts. "
                "I will provide you with Arabic memes and the text extracted from these images. Your task is to classify the image as one of the following: "
                "'propaganda', 'not-propaganda', 'not-meme', or 'other', and provide a brief explanation in Arabic. "
                "Start your response with 'Label:' followed by the classification label, then on a new line begin with 'Explanation:' and briefly state your reasoning."
            ),
            "explanation_en": (
                "You are an expert social media image analyzer specializing in identifying propaganda in Arabic contexts. "
                "I will provide you with Arabic memes and the text extracted from these images. Your task is to classify the image as one of the following: "
                "'propaganda', 'not-propaganda', 'not-meme', or 'other', and provide a brief explanation in English. "
                "Start your response with 'Label:' followed by the classification label, then on a new line begin with 'Explanation:' and briefly state your reasoning."
            )
        }

    else:  # hateful
        SYS_PROMPT = "You are an expert social media image analyzer specializing in identifying hateful content in memes"
        INSTRUCTION_CLS = (
            "I will provide you with memes and the text extracted from these images. Your task is to classify the image as one of the following: "
            "'hateful' or 'non-hateful'. Return only the label, and start your response with 'Label:' followed by the classification label."
        )
        INSTRUCTIONS_EXP = {
            "explanation": (
                "I will provide you with memes and the text extracted from these images. Your task is to classify the image as one of the following: "
                "'hateful' or 'non-hateful' and provide a brief explanation. "
                "Start your response with 'Label:' followed by the classification label, then on a new line begin with 'Explanation:' and briefly state your reasoning."
            )
        }

    for split in ["train", "test", "dev"]:
        # classification
        formatted = format_data(dataset[split], INSTRUCTION_CLS, SYS_PROMPT, "classification", args.data_base_path)
        save_jsonl(formatted, os.path.join(args.output_dir, "classification", f"{split}.jsonl"))

        # explanation
        for exp_key, instruction in INSTRUCTIONS_EXP.items():
            formatted = format_data(
                dataset[split],
                instruction,
                SYS_PROMPT,
                "explanation",
                args.data_base_path,
                explanation_column=exp_key
            )
            save_jsonl(formatted, os.path.join(args.output_dir, "explanation", exp_key, f"{split}.jsonl"))
