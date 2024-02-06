import base64
from openai import OpenAI

client = OpenAI(api_key=open('openai-api.key').readline())

with open('04-image.jpg', 'rb') as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

response = client.chat.completions.create(
    model='gpt-4-vision-preview',
    messages=[{
        'role': 'user',
        'content': [{
            'type': 'text',
            'text': 'What’s in this image?',
            # 'text': 'Co jest na obrazku?',
        }, {
            'type': 'image_url',
            'image_url': {
                'url': f'data:image/jpeg;base64,{base64_image}'
            },
        }],
    }],
    max_tokens=100,
)

print(response.choices[0].message.content)
