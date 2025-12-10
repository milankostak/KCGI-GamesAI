import base64
import json

from anthropic import Anthropic

api_key = "anthropic_api_key_here"
client = Anthropic(api_key=api_key)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image("img.png")
media_type = "image/png"

# noinspection PyTypeChecker
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": base64_image,
                    },
                },
                {
                    "type": "text",
                    "text": "What's in this image?"
                }
            ],
        }
    ],
)

print(message)

pretty_json = json.dumps(json.loads(message.model_dump_json()), indent=2)
print(pretty_json)
