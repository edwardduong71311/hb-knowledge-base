import chromadb

CHROMA_COLLECTION = "diseases"
client = chromadb.PersistentClient(path="chromadb_data")


def get_create_collection():
    return client.get_or_create_collection(
        name=CHROMA_COLLECTION, metadata={"hnsw:space": "cosine"}
    )


def reset_collection():
    client.get_or_create_collection(name=CHROMA_COLLECTION).delete()
    get_create_collection()


def add_collection(ids, metadatas, embeddings):
    collection = get_create_collection()
    collection.add(embeddings=embeddings, metadatas=metadatas, ids=ids)


def query_collection(query, threshold: float = 0.7):
    collection = get_create_collection()
    res = collection.query(
        query_embeddings=[query], n_results=10, include=["metadatas", "distances"]
    )

    data = []
    scores = []
    for index in range(len(res["distances"][0])):
        # Distance = 1 - cosine_similarity
        # Distance to Score = 1 - Distance
        score = 1 - res["distances"][0][index]
        if score > threshold:
            scores.append(score)
            data.append(res["metadatas"][0][index])

    return {"metadatas": data, "scores": scores}
