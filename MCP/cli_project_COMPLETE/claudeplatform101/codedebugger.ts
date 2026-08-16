import Anthropic from "@anthropic-ai/sdk";
import "dotenv/config";

const client = new Anthropic();

const buggyCode = `
function add(a, b) {
  return a - b;
}
`;

async function main() {
  const response = await client.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 1024,
    system: "You are a terse senior code reviewer. Give feedback in one paragraph.",
    messages: [
      { role: "user", content: `Review this code:\n${buggyCode}` },
    ],
  });

  for (const block of response.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
}

main();
