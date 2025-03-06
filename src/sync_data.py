import json

import requests

from src.config.config import settings
from src.models.Disease import Disease, DiseaseSpecialties
from src.models.Hospital import HospitalSpecialists
from src.models.Specialist import SpecialistSpecialty
from src.models.Specialty import SpecialtyModel


def read_disease(obj):
    return Disease(obj["disease"], obj["common_symptom"], obj["treatment"])


def read_disease_specialties(obj):
    return DiseaseSpecialties(obj["disease"], obj["specialties"])


def read_hospital_specialists(obj):
    return HospitalSpecialists(
        obj["hospitalName"],
        obj["location"],
        obj["address"],
        obj["telephone"],
        obj["lat"],
        obj["lng"],
        obj["specialists"],
    )


def read_specialist_specialties(obj):
    return SpecialistSpecialty(obj["specialist"], obj["specialties"])


def load_disease():
    diseases_dict = {}

    try:
        with open("data/disease_database_en.json", "r", encoding="utf-8") as file:
            disease_database_en: list[Disease] = json.load(
                file, object_hook=read_disease
            )

        for itm in disease_database_en:
            diseases_dict[itm.name] = itm

    except FileNotFoundError:
        print("Error: File not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
    return diseases_dict


def load_specialty():
    diseases = []
    specialties = []

    try:
        with open("data/disease_specialty.json", "r", encoding="utf-8") as file:
            diseases: list[DiseaseSpecialties] = json.load(
                file, object_hook=read_disease_specialties
            )

        spec_set = set()
        for item in diseases:
            spec_set.update(item.specialties)

        for item in list(spec_set):
            specialties.append(SpecialtyModel(None, item, item))

    except FileNotFoundError:
        print("Error: File not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")

    return diseases, specialties


def load_hospital():
    with open("data/hospital_specialists.json", "r", encoding="utf-8") as file:
        data: list[HospitalSpecialists] = json.load(
            file, object_hook=read_hospital_specialists
        )
    return data


def load_specialist():
    specialist_dict = {}

    with open("data/specialist_specialties.json", "r", encoding="utf-8") as file:
        data: list[SpecialistSpecialty] = json.load(
            file, object_hook=read_specialist_specialties
        )

    for item in data:
        specialist_dict[item.specialist] = item

    return specialist_dict


def sync():
    diseases, specialties = load_specialty()

    # Login to server
    auth_res = requests.post(
        settings.hospital.address
        + f"/auth/login?email={settings.email}&password={settings.password}"
    )
    auth = json.loads(auth_res.text)
    headers = {"Authorization": "Bearer " + auth["data"]["token"]}

    # Process Specialty
    specialty_table = {}
    for item in specialties:
        res = requests.post(
            settings.hospital.address + "/specialties",
            headers=headers,
            json={
                "name": item.name,
                "description": item.description,
            },
        )
        spec = res.json()
        specialty_table[item.name] = SpecialtyModel(
            _id=spec["data"]["id"],
            name=spec["data"]["name"],
            description=spec["data"]["description"],
        )

    # Process Disease
    diseases_dict = load_disease()
    for disease in diseases:
        disease = {
            "name": disease.name,
            "symptom": diseases_dict[disease.name].symptom,
            "treatment": diseases_dict[disease.name].treatment,
            "specialties": [{"id": specialty_table[x].id} for x in disease.specialties],
        }
        requests.post(
            settings.hospital.address + "/diseases", headers=headers, json=disease
        )

    # Process Specialist
    specialist_dict = load_specialist()
    for specialist_name in specialist_dict:
        disease = {
            "name": specialist_name,
            "specialties": [
                {"id": specialty_table[x].id}
                for x in specialist_dict[specialist_name].specialties
            ],
        }
        res = requests.post(
            settings.hospital.address + "/specialists", headers=headers, json=disease
        )
        specialist_dict[specialist_name].id = res.json()["data"]["id"]

    # Process hospital
    hospitals: list[HospitalSpecialists] = load_hospital()
    for hospital in hospitals:
        data = {
            "name": hospital.name,
            "address": hospital.address,
            "telephone": hospital.telephone,
            "longitude": hospital.lng,
            "latitude": hospital.lat,
            "specialists": [
                {"id": specialist_dict[x].id} for x in hospital.specialists
            ],
        }
        requests.post(
            settings.hospital.address + "/hospitals", headers=headers, json=data
        )

    print("Sync done")


sync()
