import json

from openai import OpenAI

openai_client = OpenAI(api_key=open('openai-api.key').readline())

with open('06-dataset.json') as input_file:
    dataset = json.load(input_file)

embeddings = []

for entry in dataset:
    vector = openai_client.embeddings.create(
        input=entry['text'],
        model='text-embedding-ada-002'
    ).data[0].embedding

    embeddings.append({
        'title': entry['title'],
        'text': entry['text'],
        'embedding': vector
    })

with open('06-embeddings.json', 'w') as output_file:
    json.dump(embeddings, output_file)
