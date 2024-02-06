import os
import random
import textwrap

import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from openai import OpenAI

client = OpenAI(api_key=open('../src/openai-api.key').readline())
wrapper = textwrap.TextWrapper(width=50)

name = 'Bartek'

ikea_name = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{
        'role': 'system',
        'content': 'Twoim zadaniem jest stworzenie nazwy produktu w stylu IKEA, na podstawie imienia,'
                   'poprzez przeczytanie go od tyłu i dodanie do pierwszej samogłoski umlautu.'
                   'Nie dodawaj żadnych innych informacji, po prostu wypisz nazwę wielkimi literami.'
                   '---'
                   'Q: Marcin'
                   'A: NÏCRAM'
                   'Q: zuza'
                   'A: ÄZUZ'
                   'Q: KAZIMIERZ'
                   'A: ZRËIMIZAK'
    }, {
        'role': 'user',
        'content': name
    }],
    max_tokens=128
).choices[0].message.content

print(ikea_name)

product_description = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{
        'role': 'system',
        'content': 'Twoim zadaniem jest wymyślanie opisów do produktów w stylu IKEA,'
                   'będę Ci podawał nazwy, a Ty masz wymyślić ich krótki, jednolinijkowy opis katalogowy.'
                   'Nie powtarzaj nazwy produktu w opisie'
                   'Nie dodawaj znaków przestankowych'
    }, {
        'role': 'user',
        'content': ikea_name
    }],
    max_tokens=256,
).choices[0].message.content

print(product_description)

response = client.images.generate(
    model='dall-e-3',
    prompt=f'Proste, minimalistyczne, fotorealistyczne zdjęcie produktu w stylu IKEA,'
           f'przestawiające go na tle mieszkania, bez żadnych dodatkowych napisów.'
           f'Opis produktu: {product_description}',
    size="1024x1024",
    quality="standard",
    n=1,
)

image_url = response.data[0].url
image_data = requests.get(image_url).content

counter = 0
image_plain_filename = f'{name}-{counter:02}.png'

while os.path.exists(image_plain_filename):
    counter += 1
    image_plain_filename = f'{name}-{counter:02}.png'

with open(image_plain_filename, 'wb') as image_file:
    image_file.write(image_data)

image = Image.open(image_plain_filename)

# check for brightness
cropped = image.crop((0, 0, 512, 512))
greyscale_image = cropped.convert('L')
histogram = greyscale_image.histogram()
pixels = sum(histogram)
brightness = scale = len(histogram)

for index in range(0, scale):
    ratio = histogram[index] / pixels
    brightness += ratio * (-scale + index)

print(brightness / scale)

if brightness / scale > 0.5:
    color = (0, 0, 0)
else:
    color = (255, 255, 255)

# draw: name, description, price
image_draw = ImageDraw.Draw(image)

description_wrapped = wrapper.fill(text=product_description)
price = random.choice(['39,99', '59,99', '79,99', '129,99'])

image_draw.text((50, 50), ikea_name, fill=color,
                font=ImageFont.truetype('verdanab.ttf', size=60))
image_draw.text((53, 130), description_wrapped, fill=color,
                font=ImageFont.truetype('verdana.ttf', size=30))
image_draw.text((45, 160 + description_wrapped.count('\n') * 30), text=price, fill=color,
                font=ImageFont.truetype('verdanab.ttf', size=120))

image_full_filename = f'{name}-ikea-{counter:02}.jpg'
image.save(image_full_filename)
