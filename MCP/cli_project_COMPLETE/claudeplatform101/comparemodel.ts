import Anthropic from "@anthropic-ai/sdk";
import "dotenv/config";

const client = new Anthropic();

const prompt = "Explain quantum computing in one sentence.";

const models = ["claude-haiku-4-5", "claude-sonnet-4-6", "claude-opus-4-7"];

async function main() {
  for (const model of models) {
    const start = Date.now();

    const response = await client.messages.create({
      model: model,
      max_tokens: 300,
      messages: [{ role: "user", content: prompt }],
    });

    const elapsed = Date.now() - start;

    console.log(
      `[${model}] ${elapsed}ms in=${response.usage.input_tokens} out=${response.usage.output_tokens}`
    );

    for (const block of response.content) {
      if (block.type === "text") {
        console.log(block.text);
      }
    }

    console.log(); // blank line between models
  }
}

main();
