from fastapi import FastAPI
from pydantic import BaseModel

from src.app.chroma_db import query_collection

app = FastAPI()


class Disease(BaseModel):
    embeddings: list[float]


@app.post("/disease")
def read_item(disease: Disease):
    return {**query_collection(disease.embeddings)}
