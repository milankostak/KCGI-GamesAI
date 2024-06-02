from openai import OpenAI

api_key = "openai_api_key_here"
client = OpenAI(api_key=api_key)

# https://platform.openai.com/docs/guides/speech-to-text
audio_file = open("speech.mp3", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
print(transcription.text)
