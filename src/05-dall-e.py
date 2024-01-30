from openai import OpenAI
import requests

client = OpenAI(api_key=open('openai-api.key').readline())

response = client.images.generate(
  model="dall-e-3",
  prompt='A blue rubber duck, on white background, with "j-labs" written on it.',
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
image_data = requests.get(image_url).content

with open('05-image.jpg', 'wb') as image_file:
    image_file.write(image_data)
