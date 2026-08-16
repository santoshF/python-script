import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


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

    return model, tokenizer


def create_pipeline(model, tokenizer):
    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=DEVICE,
        return_full_text=False,
        max_new_tokens=50,
        do_sample=False,
    )


def generate(pipe, prompt: str, max_new_tokens: int = 256, temperature: float = 0.7):
    messages = [{"role": "user", "content": prompt}]
    output = pipe(
        messages,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=temperature > 0,
    )
    return output[0]["generated_text"]


if __name__ == "__main__":
    print("Loading model and tokenizer...")
    model, tokenizer = load_model_and_tokenizer()

    print("Creating pipeline...")
    pipe = create_pipeline(model, tokenizer)

    prompt = "Write an email apologizing to sarah for the tragic gardening mishap. explain how it happened."
    print(f"\nPrompt: {prompt}")
    response = generate(pipe, prompt, max_new_tokens=50)
    print(f"Response: {response}")
