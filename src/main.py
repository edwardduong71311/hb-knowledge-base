from fastapi import FastAPI
from pydantic import BaseModel

from src.app.chroma_db import query_collection

app = FastAPI()


class Disease(BaseModel):
    embeddings: list[list[float]]


@app.post("/diseases")
def read_item(disease: Disease):
    return {**query_collection(disease.embeddings)}
