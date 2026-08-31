"""
Convert text into embeddings with sentence-transformers/all-mpnet-base-v2,
then train a logistic regression classifier on top of them.

Usage:
    python3 embeddings.py

Requires: pip install sentence-transformers torch scikit-learn
"""

import torch
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

MODEL = "sentence-transformers/all-mpnet-base-v2"


def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"

    model = SentenceTransformer(MODEL, device=device)

    data = load_dataset("rotten_tomatoes")
    texts = data["train"]["text"]
    labels = data["train"]["label"]

    embeddings = model.encode(texts, show_progress_bar=True)
    print(f"embeddings.shape={embeddings.shape}")

    for text, embedding in zip(texts[:5], embeddings[:5]):
        print(f"{text!r} -> shape={embedding.shape}, first 5 dims={embedding[:5]}")

    clf = LogisticRegression(max_iter=1000)
    clf.fit(embeddings, labels)

    unseen_text = "A gripping, thought-provoking film with career-best performances."
    unseen_embedding = model.encode([unseen_text])
    prediction = clf.predict(unseen_embedding)[0]

    print(f"\nUnseen text: {unseen_text!r}")
    print(f"Predicted label: {prediction} ({'positive' if prediction == 1 else 'negative'})")


if __name__ == "__main__":
    main()
