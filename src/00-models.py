from pprint import pprint
from openai import OpenAI
client = OpenAI(api_key=open('openai-api.key').readline())

models = [model.id for model in client.models.list().data]
pprint(sorted(models))

