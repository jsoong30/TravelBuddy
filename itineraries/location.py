#creatir pattern
class LocationCreator:
    @staticmethod
    def create_location(data):
            return Location(
                name=data["name"],
                address=data["address"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                visit_date=data["visit_date"],
                notes=data.get("notes", ""),
                order=data.get("order", 0)
            )
class Location:
    def __init__(self, name, address, latitude, longitude, visit_date, notes='', order=0):
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.visit_date = visit_date
        self.notes = notes
        self.order = order

    def serialize(self):
        return {
            "name": self.name,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "visit_date": self.visit_date,
            "notes": self.notes,
            "order": self.order,
        }