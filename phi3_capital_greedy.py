import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "microsoft/phi-3-mini-4k-instruct"

if torch.backends.mps.is_available():
    DEVICE = "mps"
    DTYPE = torch.float16
elif torch.cuda.is_available():
    DEVICE = "cuda"
    DTYPE = torch.float16
else:
    DEVICE = "cpu"
    DTYPE = torch.float32


def load_model_and_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=DTYPE,
        trust_remote_code=True,
    ).to(DEVICE)
    model.eval()

    return model, tokenizer


if __name__ == "__main__":
    prompt = "the capital of france is"

    print("Loading model and tokenizer...")
    model, tokenizer = load_model_and_tokenizer()

    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        # output of the base transformer (before lm_head)
        model_output = model.model(**inputs)
        last_hidden_state = model_output.last_hidden_state

        # output of lm_head applied to the base model's hidden states
        lm_head_output = model.lm_head(last_hidden_state)

        # greedy decoding
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=10,
            do_sample=False,
        )

    next_token_id = lm_head_output[0, -1].argmax(dim=-1)
    response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    print(f"\nPrompt: {prompt}")
    print(f"model output (last_hidden_state) shape: {tuple(last_hidden_state.shape)}")
    print(f"lm_head output (logits) shape: {tuple(lm_head_output.shape)}")
    print(f"lm_head greedy next token: {tokenizer.decode(next_token_id)!r}")
    print(f"\nGreedy decoding output: {response}")
