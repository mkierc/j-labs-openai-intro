from openai import OpenAI

client = OpenAI(api_key=open('openai-api.key').readline())

audio_file = "02-audio-example.mp3"
tts = client.audio.speech.create(
  model="tts-1",
  # model="tts-1-hd",

  # voice="alloy",
  # voice="echo",
  # voice="fable",
  voice="onyx",
  # voice="nova",
  # voice="shimmer",

  input="Serdeczne pozdrowienia dla wszystkich gości na prezentacji!"
)

tts.stream_to_file(audio_file)
