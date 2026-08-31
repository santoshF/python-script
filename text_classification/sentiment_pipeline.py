"""
Run sentiment analysis with cardiffnlp/twitter-roberta-base-sentiment-latest.

Usage:
    python3 sentiment_pipeline.py

Requires: pip install transformers torch
"""

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"


def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    sentiment = pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer,
        device=device,
        return_all_scores=True,
    )

    texts = [
        "I love this new phone, it's amazing!",
        "This is the worst service I've ever experienced.",
        "The weather today is okay, nothing special.",
    ]

    for text in texts:
        result = sentiment(text)
        print(f"{text!r} -> {result}")


if __name__ == "__main__":
    main()
