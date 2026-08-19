import torch
from transformers import AutoTokenizer, AutoModel


TOKENIZER_ID = "microsoft/deberta-base"
MODEL_ID = "microsoft/deberta-v3-xsmall"


def load_tokenizer():
    return AutoTokenizer.from_pretrained(TOKENIZER_ID)


def load_model():
    return AutoModel.from_pretrained(MODEL_ID)


def tokenize(tokenizer, sentence: str):
    return tokenizer(sentence, return_tensors="pt")


def process_tokens(model, inputs):
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state


if __name__ == "__main__":
    print("Loading tokenizer...")
    tokenizer = load_tokenizer()

    print("Loading model...")
    model = load_model()

    sentence = "Hello World"
    inputs = tokenize(tokenizer, sentence)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    print(f"\nSentence: {sentence}")
    print(f"Token IDs: {inputs['input_ids'][0].tolist()}")
    print(f"Tokens: {tokens}")

    hidden_states = process_tokens(model, inputs)
    print(f"Output hidden states shape: {tuple(hidden_states.shape)}")
