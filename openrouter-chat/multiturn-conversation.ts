import { OpenRouter } from '@openrouter/sdk';
import * as readline from 'node:readline';

const client = new OpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
});

const messages: { role: 'user' | 'assistant'; content: string }[] = [];

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function ask(): void {
  rl.question('You: ', async (input) => {
    if (input.toLowerCase() === 'exit') {
      rl.close();
      return;
    }

    messages.push({ role: 'user', content: input });

    const stream = await client.chat.send({
      chatRequest: {
        model: 'google/gemini-3.1-flash-lite',
        messages,
        stream: true,
      },
    });

    let response = '';
    process.stdout.write('Assistant: ');
    for await (const chunk of stream) {
      const delta = chunk.choices[0]?.delta?.content;
      if (delta) {
        process.stdout.write(delta);
        response += delta;
      }
    }
    console.log();

    messages.push({ role: 'assistant', content: response });
    ask();
  });
}

ask();

