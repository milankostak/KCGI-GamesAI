import json

from openai import OpenAI

api_key = "openai_api_key_here"
client = OpenAI(api_key=api_key)

# https://platform.openai.com/docs/guides/text-generation
response = client.chat.completions.create(
    model="gpt-4o",
    # temperature=0.7,  # 0.0 is deterministic, 2.0 is maximum entropy, 1.0 is the default value
    # max_tokens=1000,  # maximum number of tokens to generate
    # stop=["and"],     # stop the generation when the token is generated
    messages=[
        {"role": "system", "content": "You are a helpful assistant knowledgeable about the application of machine learning in video games. You provide explanation to a university student."},
        {"role": "user", "content": "Can you explain how reinforcement learning is used in video games?"},
        {"role": "assistant", "content": "Certainly! Reinforcement learning (RL) is used in video games to train AI agents to make decisions by rewarding desired actions and penalizing undesirable ones. For example, in a game like 'StarCraft II', RL can be used to train AI agents to execute complex strategies based on the state of the game. The AI learns through trial and error, gradually improving its strategy to maximize rewards, which could be points, victories, or achieving specific objectives within the game."},
        {"role": "user", "content": "What's a real-world example of a game that uses RL?"},
    ]
)
print(response)

pretty_json = json.dumps(json.loads(response.model_dump_json()), indent=2)
print(pretty_json)
