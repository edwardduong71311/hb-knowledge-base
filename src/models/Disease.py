from dataclasses import dataclass


@dataclass
class Disease:
    def __init__(self, name: str, symptom: str, treatment: str):
        self.name = name
        self.symptom = symptom
        self.treatment = treatment


class DiseaseSpecialties:
    def __init__(self, name: str, specialties: list[str]):
        self.name = name
        self.specialties = specialties
