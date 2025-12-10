import json

from anthropic import Anthropic

api_key = "anthropic_api_key_here"
client = Anthropic(api_key=api_key)

# https://platform.claude.com/docs/en/api/overview#client-sdks
message = client.messages.create(
    model="claude-sonnet-4-5",
    temperature=0.7,  # 0.0 is deterministic, 1.0 is maximum entropy
    max_tokens=1000,  # maximum number of tokens to generate
    system="You are a helpful assistant knowledgeable about the application of machine learning in video games.",
    messages=[
        {"role": "user", "content": "Can you explain how reinforcement learning is used in video games?"},
    ]
)
print(message)

pretty_json = json.dumps(json.loads(message.model_dump_json()), indent=2)
print(pretty_json)
