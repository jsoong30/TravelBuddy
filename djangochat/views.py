from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room
from django.shortcuts import render

# Create your views here.
@login_required
def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'room/room.html', {'room': room})