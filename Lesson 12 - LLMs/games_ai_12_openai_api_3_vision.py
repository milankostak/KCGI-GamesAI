import base64
import json

from openai import OpenAI

api_key = "openai_api_key_here"
client = OpenAI(api_key=api_key)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image("img.png")

# https://platform.openai.com/docs/guides/images-vision?format=base64-encoded
# noinspection PyTypeChecker
response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "what's in this image?"},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ],
)

print(response)

pretty_json = json.dumps(json.loads(response.model_dump_json()), indent=2)
print(pretty_json)
