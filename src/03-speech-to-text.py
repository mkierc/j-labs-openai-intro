from openai import OpenAI

client = OpenAI(api_key=open('openai-api.key').readline())

# audio_file = open("02-audio-example.mp3", "rb")
audio_file = open("03-audio-example-marszalek.mp3", "rb")

stt = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file
)

print(stt.text)
