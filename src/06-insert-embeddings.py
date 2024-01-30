import json
from pprint import pprint

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

qdrant_client = QdrantClient('localhost', port=6333)

qdrant_client.recreate_collection(
    collection_name='j-labs-embedding-articles',
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

with open('06-embeddings.json') as json_file:
    dataset_mapping = json.load(json_file)
# with open('06-embeddings-prepared.json') as json_file:
#     dataset_mapping = json.load(json_file)

data_points = [PointStruct(
    id=_id,
    vector=entry['embedding'],
    payload={
        'title': entry['title'],
        'text': entry['text']
    })
    for _id, entry in enumerate(dataset_mapping)
]

pprint(data_points)

qdrant_client.upsert(
    collection_name='j-labs-embedding-articles',
    points=data_points
)

print(qdrant_client.get_collection('j-labs-embedding-articles'))
