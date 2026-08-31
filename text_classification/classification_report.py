"""
Run textattack/bert-base-uncased-rotten-tomatoes over the rotten_tomatoes
test split and print a classification report.

Usage:
    python3 classification_report.py

Requires: pip install transformers torch datasets scikit-learn
"""

import torch
from datasets import load_dataset
from sklearn.metrics import classification_report
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from transformers.pipelines.pt_utils import KeyDataset

MODEL = "textattack/bert-base-uncased-rotten-tomatoes"


def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    sentiment = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)

    label_to_id = {label: idx for idx, label in model.config.id2label.items()}

    test_data = load_dataset("rotten_tomatoes")["test"]

    predictions = [
        label_to_id[result["label"]]
        for result in tqdm(sentiment(KeyDataset(test_data, "text")), total=len(test_data))
    ]

    report = classification_report(
        test_data["label"], predictions, target_names=["negative", "positive"]
    )
    print(report)


if __name__ == "__main__":
    main()
