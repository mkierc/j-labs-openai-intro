from openai import OpenAI
from qdrant_client import QdrantClient

openai_client = OpenAI(api_key=open('openai-api.key').readline())
qdrant_client = QdrantClient("localhost", port=6333)


# query = "How to use AWS lambda?"
# query = "What can I do with elastic search?"
# query = "concurent code slow, help"
query = "how to get rich fast learning it"
# query = "Do czego mogę użyć elastik searcha?"

query_vector = openai_client.embeddings.create(
    input=query,
    model='text-embedding-ada-002'
).data[0].embedding

hits = qdrant_client.search(
    collection_name="j-labs-embedding-articles",
    query_vector=query_vector,
    limit=10
)

similarity_hard_cutoff = 0.75
similarity_soft_cutoff = hits[0].score - 0.05

for hit in hits:
    if hit.score < similarity_soft_cutoff or hit.score < similarity_hard_cutoff:
        break
    text = hit.payload["text"].replace('\n', '')
    print(f'score: {hit.score}, title: {hit.payload["title"]}, text: {text}')
