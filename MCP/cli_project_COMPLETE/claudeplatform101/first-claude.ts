import Anthropic from "@anthropic-ai/sdk";
import "dotenv/config";

const client = new Anthropic();

async function main() {
  const msg = await client.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "Hello, Claude",
      },
    ],
  });

  console.log(msg.content);
}

main();
