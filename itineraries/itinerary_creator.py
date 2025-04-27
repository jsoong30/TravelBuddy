from .models import Itinerary
from .location import LocationCreator
import json
class ItineraryCreator:
    @staticmethod
    def create(user, title, raw_locations, start_date, end_date):
        serialized_locations = [
            LocationCreator.create_location(loc).serialize() for loc in json.loads(raw_locations)
        ]
        itinerary = Itinerary.objects.create(
            user=user,
            name=title,
            start_date=start_date,
            end_date=end_date,
            locations=serialized_locations
        )

        return itinerary