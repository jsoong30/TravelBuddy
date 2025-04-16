# chat/urls.py
from django.urls import path
from .views import rooms_list, create_room, room

urlpatterns = [
    path('', rooms_list, name='rooms_list'),
    path('create/', create_room, name='create_room'),
    path('<slug:room_slug>/', room, name='room'),
]
