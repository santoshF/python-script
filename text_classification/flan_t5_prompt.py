"""
Prompt-based sentiment classification with google/flan-t5-small: run inference
over the rotten_tomatoes test split and evaluate against the true labels.

Usage:
    python3 flan_t5_prompt.py

Requires: pip install transformers torch datasets scikit-learn tqdm
"""

import torch
from datasets import load_dataset
from sklearn.metrics import classification_report
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from transformers.pipelines.pt_utils import KeyDataset

MODEL = "google/flan-t5-small"
PROMPT_TEMPLATE = "Classify the sentiment of this movie review as positive or negative: {text}"


def add_prompt(example):
    example["prompt"] = PROMPT_TEMPLATE.format(text=example["text"])
    return example


def parse_prediction(generated_text):
    return 1 if "positive" in generated_text.lower() else 0


def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
    generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=device)

    test_data = load_dataset("rotten_tomatoes")["test"].map(add_prompt)

    predictions = [
        parse_prediction(result[0]["generated_text"])
        for result in tqdm(generator(KeyDataset(test_data, "prompt")), total=len(test_data))
    ]

    report = classification_report(
        test_data["label"], predictions, target_names=["negative", "positive"]
    )
    print(report)


if __name__ == "__main__":
    main()
