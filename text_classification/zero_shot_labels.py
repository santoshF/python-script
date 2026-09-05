"""
Zero-shot classification via label embeddings: encode the label names
themselves with sentence-transformers/all-mpnet-base-v2 and classify texts
by cosine similarity, without training a classifier.

Usage:
    python3 zero_shot_labels.py

Requires: pip install sentence-transformers torch
"""

import torch
from sentence_transformers import SentenceTransformer, util

MODEL = "sentence-transformers/all-mpnet-base-v2"
LABELS = [
    "a negative, unfavorable movie review",
    "a positive, favorable movie review",
]


def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = SentenceTransformer(MODEL, device=device)

    label_embeddings = model.encode(LABELS)

    texts = [
        "A gripping, thought-provoking film with career-best performances.",
        "A tedious, poorly acted mess that wastes its own premise.",
    ]
    text_embeddings = model.encode(texts)

    similarities = util.cos_sim(text_embeddings, label_embeddings)
    predictions = similarities.argmax(dim=1)

    for text, prediction in zip(texts, predictions):
        print(f"{text!r} -> {LABELS[prediction]}")


if __name__ == "__main__":
    main()
