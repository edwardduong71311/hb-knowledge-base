class HospitalSpecialists:
    def __init__(
        self,
        name: str,
        location: str,
        address: str,
        telephone: str,
        lat: float,
        lng: float,
        specialists: list[str],
    ):
        self.name = name
        self.location = location
        self.address = address
        self.telephone = telephone
        self.lat = lat
        self.lng = lng
        self.specialists = specialists
