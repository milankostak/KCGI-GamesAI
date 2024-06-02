import json

from openai import OpenAI

api_key = "openai_api_key_here"
client = OpenAI(api_key=api_key)

# https://platform.openai.com/docs/guides/images
response = client.images.generate(
    model="dall-e-3",
    prompt="Games and Artificial Intelligence",
    # size="1792x1024",
    size="1024x1024",
    # quality="hd",
    quality="standard",
    style="natural",
    n=1,
)
# One image in this quality (standard) and resolution (1024x1024) costs around 6-7 JPY

print(response)

pretty_json = json.dumps(json.loads(response.json()), indent=2)
print(pretty_json)

# image_url = response.data[0].url
# print(image_url)
