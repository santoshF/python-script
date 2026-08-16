from sentence_transformers import SentenceTransformer


MODEL_ID = "sentence-transformers/all-mpnet-base-v2"


def load_model():
    return SentenceTransformer(MODEL_ID)


def embed(model, sentences):
    return model.encode(sentences)


if __name__ == "__main__":
    print("Loading model...")
    model = load_model()

    sentences = ["best movie ever"]

    embeddings = embed(model, sentences)

    for sentence, embedding in zip(sentences, embeddings):
        print(f"\nSentence: {sentence}")
        print(f"Embedding shape: {embedding.shape}")
        print(f"First 5 values: {embedding[:5]}")
