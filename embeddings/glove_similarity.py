import gensim.downloader as api


MODEL_ID = "glove-wiki-gigaword-50"


def load_model():
    return api.load(MODEL_ID)


def most_similar(model, word: str, top_n: int = 15):
    return model.most_similar(word, topn=top_n)


if __name__ == "__main__":
    print("Loading model...")
    model = load_model()

    word = "king"
    similar_words = most_similar(model, word, top_n=15)

    print(f"\nMost similar words to '{word}':")
    for similar_word, score in similar_words:
        print(f"{similar_word}: {score:.4f}")
