import { OpenRouter } from '@openrouter/sdk';

const client = new OpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
});

const stream = await client.chat.send({
  chatRequest: {
    model: 'openrouter/free',
    messages: [
      { role: 'user', content: 'Explain how routers work in three sentences.' },
    ],
    stream: true,
  },
});

for await (const chunk of stream) {
  const delta = chunk.choices[0]?.delta?.content;
  if (delta) process.stdout.write(delta);
}
console.log();

