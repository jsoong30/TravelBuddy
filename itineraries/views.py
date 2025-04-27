from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from djangochat.models import Room
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Itinerary
from .itinerary_creator import ItineraryCreator
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import math
from datetime import datetime

def distance_haversine(lat1, lon1, lat2, lon2):
    Radius = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = Radius * c
    return distance

def itinerary_list(request):
    itineraries = Itinerary.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    location = request.GET.get('location')
    user_lat = request.GET.get('lat')
    user_lon = request.GET.get('lon')

    if not user_lat or not user_lon:
        user_lat = 33.7490  # Default to Atlanta
        user_lon = -84.3880
    else:
        user_lat = float(user_lat)
        user_lon = float(user_lon)

    if start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            itineraries = itineraries.filter(
                start_date__lte=end_date_obj,
                end_date__gte=start_date_obj
            )
        except ValueError:
            pass

    itinerary_list_with_distance = []
    for itinerary in itineraries:
        if itinerary.locations:
            loc = itinerary.locations[0]  # Assume first location is main
            lat = loc.get('latitude')
            lon = loc.get('longitude')
            if lat is not None and lon is not None:
                distance = distance_haversine(user_lat, user_lon, lat, lon)
                itinerary_list_with_distance.append((distance, itinerary))

    itinerary_list_with_distance.sort(key=lambda x: x[0])

    sorted_itineraries = [it[1] for it in itinerary_list_with_distance]

    return render(request, 'itinerary_list.html', {
        'itineraries': sorted_itineraries,
        'start_date': start_date,
        'end_date': end_date,
        'location': location,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    })
def view_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    is_owner = request.user.is_authenticated and itinerary.user == request.user
    locations = itinerary.locations

    locations_json = json.dumps(locations)
    return render(request, 'itinerary.html', {
        'itinerary': itinerary,
        'is_owner': is_owner,
        'locations': locations_json,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    })
def delete_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    if itinerary.user == request.user:
        itinerary.delete()
        return redirect('home')
    else:
        raise PermissionDenied

@login_required
def create_itinerary(request, itinerary_id=None):
    if itinerary_id:
        itinerary = get_object_or_404(Itinerary, id=itinerary_id)

        if request.user != itinerary.user:
            return redirect('view_itinerary', itinerary_id=itinerary.id)
    else:
        itinerary = None

    if request.method == "POST":
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        locations_json = request.POST.get('locations_json')

        if itinerary:
            itinerary.title = title
            itinerary.start_date = start_date
            itinerary.end_date = end_date
            itinerary.locations_json = locations_json
        else:
            itinerary = ItineraryCreator.create(
                user=request.user,
                title=title,
                raw_locations=locations_json,
                start_date=start_date,
                end_date=end_date
            )


        itinerary.save()

        return redirect('view_itinerary', itinerary_id=itinerary.id)

    context = {
        'itinerary': itinerary,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'create_itinerary.html', context)