# chat/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom
from .forms import ChatRoomForm

def rooms_list(request):
    """List all available chat rooms."""
    chat_rooms = ChatRoom.objects.all()
    context = {
        'chat_rooms': chat_rooms,
        'page_title': 'Chat Rooms'
    }
    return render(request, 'rooms_list.html', context)

@login_required(login_url='/login/')
def create_room(request):
    if request.method == "POST":
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chat_room = form.save(commit=False)
            chat_room.created_by = request.user
            chat_room.save()
            return redirect('room', room_slug=chat_room.slug)
    else:
        form = ChatRoomForm()
    context = {
        'form': form,
        'page_title': 'Create Chat Room'
    }
    return render(request, 'create_room.html', context)

def room(request, room_slug):
    room = get_object_or_404(ChatRoom, slug=room_slug)
    context = {
        'room': room,
        'page_title': f'Chat Room: {room.name}'
    }
    return render(request, 'room.html', context)
