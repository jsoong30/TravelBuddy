from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Room, Message, RoomMembership
from django.utils.text import slugify

# Create your views here.
@login_required
def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    try:
        membership = RoomMembership.objects.get(room=room, user=request.user)
    except RoomMembership.DoesNotExist:
        membership = None

    if membership is None:
        return render(request, 'room/request_to_join.html', {'room': room})

    if membership.status == RoomMembership.PENDING:
        return render(request, 'room/pending.html', {'room': room})

    if membership.status == RoomMembership.DENIED:
        return render(request, 'room/denied.html', {'room': room})

    # Approved → show chat
    messages = Message.objects.filter(room=room).order_by('date_added')[:25]
    return render(request, 'room/room.html', {
        'room': room, 'messages': messages
    })

@login_required
def request_to_join(request, slug):
    room, _ = Room.objects.get_or_create(slug=slug)
    RoomMembership.objects.get_or_create(room=room, user=request.user)
    return redirect('room', slug=slug)

@login_required
def manage_requests(request, slug):
    room = get_object_or_404(Room, slug=slug, owner=request.user)
    pending = RoomMembership.objects.filter(
        room=room, status=RoomMembership.PENDING
    )
    return render(request, 'room/manage_requests.html', {
        'room': room, 'pending': pending
    })

@login_required
def change_request_status(request, slug, membership_id, new_status):
    room = get_object_or_404(Room, slug=slug, owner=request.user)
    membership = get_object_or_404(
        RoomMembership, id=membership_id, room=room
    )
    membership.status = int(new_status)
    membership.save()
    return redirect('manage_requests', slug=slug)

@login_required
def create_room(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # simple slug generation; you might want to check for uniqueness
        slug = slugify(name)
        room = Room.objects.create(
            name=name,
            slug=slug,
            owner=request.user
        )
        # auto-approve the creator
        RoomMembership.objects.create(
            user=request.user,
            room=room,
            status=RoomMembership.APPROVED
        )
        return redirect('room', slug=slug)
    return render(request, 'room/create_room.html')