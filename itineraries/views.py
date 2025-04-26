from rest_framework.generics import RetrieveAPIView
from .models import Itinerary
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from .forms import ItineraryForm

import json
from django.shortcuts import render, redirect
from .models import Itinerary
from .itinerary_creator import ItineraryCreator
from .forms import ItineraryForm

#dummy page for iteneraries
def itinerary_list(request):
    itineraries = Itinerary.objects.all()  # Fetch all itineraries from the database
    return render(request, 'itinerary_list.html', {'itineraries': itineraries})
def itinerary_map(request, itinerary_id):
    # Get itinerary object based on the ID
    itinerary = Itinerary.objects.get(id=itinerary_id)

    # Pass itinerary data and API key to template
    return render(request, 'itinerary.html', {
        'itinerary': itinerary,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    })

def create_itinerary(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        locations_json = request.POST.get('locations_json', '[]')
        raw_locations = json.loads(locations_json)

        creator = ItineraryCreator(
            user=request.user,
            title=title,
            raw_locations=raw_locations,
            start_date=start_date,
            end_date=end_date,
        )
        creator.create()

        return redirect('home')  # or itinerary detail

    return render(request, 'create_itinerary.html', {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    })