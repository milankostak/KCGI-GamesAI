import base64
import json
from datetime import datetime

from openai import OpenAI

api_key = "openai_api_key_here"
client = OpenAI(api_key=api_key)

# https://developers.openai.com/api/docs/guides/image-generation
response = client.images.generate(
    model="gpt-image-1",
    prompt="Games and Artificial Intelligence",
    size="1024x1024",  # Options: "1024x1024", "1536x1024", "1024x1536", "auto"
    quality="medium",  # Options: "low", "medium", "high", "auto"
    n=1,
)
# One image in this quality (medium) and resolution (1024x1024) costs around 6-7 JPY

pretty_json = json.dumps(json.loads(response.model_dump_json()), indent=2)
print(pretty_json)

# Returns base64 by default
image_b64: str = str(response.data[0].b64_json)

date_time: str = datetime.now().strftime("%Y%m%d_%H%M%S")
base_name = f"output_{date_time}"
ext = ".png"
filename = f"{base_name}{ext}"

with open(filename, "wb") as f:
    f.write(base64.b64decode(image_b64))

print(f"Saved: {filename}")
