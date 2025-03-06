import json
import uuid

from src.app.chroma_db import add_collection


def sync():
    with open("data/disease_embeddings.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for d in data:
        embeddings, metadatas, ids = [], [], []
        for embedding in d["embeddings"]:
            ids.append(str(uuid.uuid4()))
            metadatas.append(
                {
                    "id": d["id"],
                    "name": d["name"],
                    "symptom": d["symptom"],
                    "treatment": d["treatment"],
                }
            )
            embeddings.append(embedding)
        add_collection(ids, metadatas, embeddings)
    print("Sync done")


sync()
