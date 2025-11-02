#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
score_dataset.py
================
A configurable evaluation pipeline for JSONL datasets containing:
- classification labels
- (optionally) free-text explanations

It computes:
- Classification metrics + saves confusion matrix plot
- Explanation metrics (BERTScore, ROUGE, BLEU, METEOR) if applicable
- Outputs results as metrics.json
"""

import argparse
import json
import os
import random
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # for servers without display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch
from bert_score import score as bertscore
from nltk import download as nltk_download
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import corpus_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from transformers import AutoTokenizer
import evaluate as hf_evaluate


for pkg in ["punkt", "wordnet", "omw-1.4"]:
    nltk_download(pkg, quiet=True)

LABEL_RE = re.compile(r"Label:\s*([^\n]+)")
EXPL_RE = re.compile(r"Explanation:\s*([^\n]+)")


def extract_label_and_explanation(text: str) -> tuple[str | None, str | None]:
    """Extract Label and Explanation from a string block."""
    if pd.isna(text):
        return None, None
    label_match = LABEL_RE.search(text)
    expl_match = EXPL_RE.search(text)
    label = label_match.group(1).strip() if label_match else None
    explanation = expl_match.group(1).strip() if expl_match else None
    return label, explanation


def read_jsonl_select_columns(file_path: str | Path, columns=("response", "labels")) -> pd.DataFrame:
    df = pd.read_json(file_path, lines=True)
    if not set(columns).issubset(df.columns):
        raise ValueError(f"Missing expected columns {columns} in file {file_path}")
    return df[list(columns)]


def fix_invalid_labels(label: str | None, valid_labels: set) -> str:
    """If label is invalid or missing, randomly assign from valid_labels."""
    if label in valid_labels:
        return label
    return random.choice(list(valid_labels))


def evaluate_classification(df: pd.DataFrame,
                            gold_col: str,
                            pred_col: str,
                            cm_path: Path | None = None) -> dict:
    y_true, y_pred = df[gold_col], df[pred_col]

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "precision_weighted": precision_score(y_true, y_pred, average="weighted", zero_division=0),
        "recall_weighted": recall_score(y_true, y_pred, average="weighted", zero_division=0),
        "f1_weighted": f1_score(y_true, y_pred, average="weighted", zero_division=0),
    }

    cm = confusion_matrix(y_true, y_pred)
    labels = sorted(y_true.unique())
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='g', cmap='Blues',
                xticklabels=labels, yticklabels=labels, cbar=False)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    if cm_path:
        plt.tight_layout()
        plt.savefig(cm_path, dpi=300)
    plt.close()

    return metrics


def compute_bertscore(preds, refs, arabic=False) -> dict:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = "aubmindlab/bert-base-arabertv2" if arabic else "bert-base-multilingual-uncased"

    preds = [" ".join(str(p).split()[:1024]) for p in preds]
    refs = [" ".join(str(r).split()[:1024]) for r in refs]

    P, R, F = bertscore(
        cands=preds,
        refs=refs,
        model_type=model,
        device=device,
        num_layers=12,
        batch_size=32,
        verbose=False
    )
    return {
        "bertscore_precision": P.mean().item(),
        "bertscore_recall": R.mean().item(),
        "bertscore_f1": F.mean().item()
    }


def compute_rouge(preds, refs, arabic=False) -> dict:
    model_name = "aubmindlab/bert-base-arabertv2" if arabic else "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], tokenizer=tokenizer)
    r1, r2, rL = [], [], []

    for p, r in zip(preds, refs):
        scores = scorer.score(r, p)
        r1.append(scores["rouge1"].fmeasure)
        r2.append(scores["rouge2"].fmeasure)
        rL.append(scores["rougeL"].fmeasure)

    return {
        "rouge1": float(np.mean(r1)),
        "rouge2": float(np.mean(r2)),
        "rougeL": float(np.mean(rL))
    }


def compute_bleu_meteor(preds, refs) -> dict:
    smooth_fn = SmoothingFunction().method1
    bleu = corpus_bleu([[word_tokenize(r)] for r in refs],
                       [word_tokenize(p) for p in preds],
                       smoothing_function=smooth_fn)
    meteor_scores = [meteor_score([word_tokenize(r)], word_tokenize(p)) for r, p in zip(refs, preds)]
    return {
        "bleu": bleu,
        "meteor": float(np.mean(meteor_scores))
    }


def evaluate_explanations(preds, refs, arabic=False) -> dict:
    return {
        **compute_bertscore(preds, refs, arabic=arabic),
        **compute_rouge(preds, refs, arabic=arabic),
        **compute_bleu_meteor(preds, refs)
    }


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to JSONL dataset file")
    parser.add_argument("--has_explanation", action="store_true", help="If present, compute explanation metrics")
    parser.add_argument("--is_arabic", action="store_true", help="Use AraBERT models/tokenizers")
    parser.add_argument("--out_dir", required=True, help="Directory to save metrics.json & confusion_matrix.png")
    return parser.parse_args()


def main():
    args = cli()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = read_jsonl_select_columns(args.data)
    df[["labels_label", "labels_explanation"]] = pd.DataFrame(
        df["labels"].apply(extract_label_and_explanation).tolist(), index=df.index
    )
    df[["response_label", "response_explanation"]] = pd.DataFrame(
        df["response"].apply(extract_label_and_explanation).tolist(), index=df.index
    )

    valid_labels = set(df["labels_label"].dropna())
    if not valid_labels:
        raise ValueError("No valid gold labels found in dataset!")

    df["response_label"] = df["response_label"].apply(lambda x: fix_invalid_labels(x, valid_labels))

    ########## to normalize labels since zero-shot models may produce variations like "non-" instead of "not-"
    def normalize_non_to_not(label):
        label = label.lower()
        if isinstance(label, str) and label.startswith("non-"):
            
            label =  "not-" + label[4:]
            #print(label)
            return label
            
        return label

    df["labels_label"] = df["labels_label"].apply(normalize_non_to_not)
    df["response_label"] = df["response_label"].apply(normalize_non_to_not)
    ############
    metrics = evaluate_classification(
        df, gold_col="labels_label", pred_col="response_label",
        cm_path=out_dir / "confusion_matrix.png"
    )

    if args.has_explanation:
        preds = df["response_explanation"].fillna("").tolist()
        refs = df["labels_explanation"].fillna("").tolist()
        metrics.update(evaluate_explanations(preds, refs, arabic=args.is_arabic))

    # save
    with open(out_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print("\nEvaluation complete")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    print(f"Metrics saved to {out_dir / 'metrics.json'}")
    print(f"Confusion matrix saved to {out_dir / 'confusion_matrix.png'}")


if __name__ == "__main__":
    main()
