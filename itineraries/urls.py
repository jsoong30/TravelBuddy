from django.contrib import admin
from django.urls import path, include

from .views import view_itinerary, itinerary_list, create_itinerary, delete_itinerary

urlpatterns = [
    path('', itinerary_list, name='itinerary-list'),
    path('<int:itinerary_id>/', view_itinerary, name='view_itinerary'),
    path('create', create_itinerary, name='create_itinerary'),
    path('<int:itinerary_id>/edit/', create_itinerary, name='edit_itinerary'), #reuse create
    path('<int:itinerary_id>/delete/', delete_itinerary, name='delete_itinerary'),

]