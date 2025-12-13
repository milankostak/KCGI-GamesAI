from openai import OpenAI

api_key = "openai_api_key_here"
client = OpenAI(api_key=api_key)

# https://platform.openai.com/docs/guides/text-to-speech
speech_file_path = "speech.mp3"
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    response_format="mp3",
    input="Today is a wonderful day to build something using LLM API!"
) as response:
    response.stream_to_file(speech_file_path)
