import os
import uuid
import nltk
import json
import requests
from openai import OpenAI
from nltk.tokenize import sent_tokenize

from src.config.config import settings
from src.models.Disease import Disease

nltk.download("punkt_tab")
nltk.download("punkt")

client = OpenAI(api_key=settings.ai_token)
filename = "data/disease_embeddings.json"


def write_to_json_file(data, file_name):
    try:
        # Check if file exists; if not, it will be created automatically
        if not os.path.exists(file_name):
            print(f"File '{file_name}' does not exist. Creating new file.")

        # Write the data to the file with indentation for readability
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"Successfully wrote data to '{file_name}'.")
    except Exception as e:
        print(f"Error writing to file: {e}")


def sync():
    # Login to server
    auth_res = requests.post(
        settings.hospital.address
        + f"/auth/login?email={settings.email}&password={settings.password}"
    )
    auth = json.loads(auth_res.text)
    headers = {"Authorization": "Bearer " + auth["data"]["token"]}

    # Get diseases
    arr = []
    page = 0
    while True:
        auth_res = requests.get(
            settings.hospital.address + f"/diseases?page={page}&size=10",
            headers=headers,
        )
        auth = json.loads(auth_res.text)

        if not auth["data"] or len(auth["data"]) == 0:
            break

        print(f"Processing page {page}...")
        for item in auth["data"]:
            disease = Disease(item["name"], item["symptom"], item["treatment"])
            sentences = sent_tokenize(disease.treatment)
            phrases = [text.strip() for text in disease.symptom.split(",")]

            phrases.extend(sentences)
            cleaned_phrases = [
                text.replace("\n", " ")
                for text in phrases
                if not (text.strip().endswith(".") and text.strip()[:-1].isdigit())
            ]
            cleaned_phrases = [s.strip() for s in cleaned_phrases if s.strip()]

            res = client.embeddings.create(
                model="text-embedding-ada-002", input=cleaned_phrases
            )
            phrase_embeddings = [(item.index, item.embedding) for item in res.data]
            phrase_embeddings.sort(key=lambda x: x[0])
            embeddings = [embedding for _, embedding in phrase_embeddings]

            arr.append(
                {
                    "id": str(uuid.uuid4()),
                    "name": disease.name,
                    "symptom": disease.symptom,
                    "treatment": disease.treatment,
                    "phrase": cleaned_phrases,
                    "embeddings": embeddings,
                }
            )
        page += 1

    write_to_json_file(arr, filename)
    print("Built embeddings")


sync()
