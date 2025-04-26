from django.contrib import admin
from django.urls import path, include

from core.views import itinerary
from .views import itinerary_map, itinerary_list, create_itinerary
urlpatterns = [
    path('', itinerary_list, name='itinerary-list'),  # Shows the list of itineraries
    path('map/<int:itinerary_id>/', itinerary_map, name='itinerary-map'),  # Maps specific itinerary
    path('create/', create_itinerary, name='create_itinerary'),
]