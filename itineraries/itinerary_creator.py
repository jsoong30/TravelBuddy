from .models import Itinerary
from .location import LocationCreator

class ItineraryCreator:
    def __init__(self, user, title, raw_locations, start_date, end_date):
        self.user = user
        self.title = title
        self.raw_locations = raw_locations
        self.start_date = start_date
        self.end_date = end_date

    def create(self):
        serialized_locations = [
            LocationCreator.create_location(loc).serialize() for loc in self.raw_locations
        ]
        itinerary = Itinerary.objects.create(
            user=self.user,
            name=self.title,
            start_date=self.start_date,
            end_date=self.end_date,
            locations=serialized_locations
        )
        return itinerary