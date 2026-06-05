from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.accounts.permissions import role_required
from .models import Room, RoomType
from .serializers import RoomSerializer, RoomTypeSerializer
from .forms import RoomForm


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


@login_required
@role_required(['super_admin', 'owner', 'manager', 'receptionist', 'housekeeping'])
def room_list(request):
    """Staff/Admin view – lists all rooms."""
    rooms = Room.objects.select_related('room_type').all()
    return render(request, 'hotel/room_list.html', {'rooms': rooms})


def room_list_public(request):
    """Public view – shows only available rooms."""
    rooms = Room.objects.select_related('room_type').filter(status='available')
    return render(request, 'hotel/room_list_public.html', {'rooms': rooms})


@login_required
@role_required(['super_admin', 'owner', 'manager', 'receptionist', 'housekeeping'])
def room_detail(request, room_number):
    room = get_object_or_404(Room.objects.select_related('room_type'), room_number=room_number)
    return render(request, 'hotel/room_detail.html', {'room': room})


@login_required
@role_required(['super_admin', 'owner', 'manager', 'housekeeping'])
def floor_list(request):
    rooms = Room.objects.select_related('room_type').all()
    # Group by floor
    floor_dict = {}
    for room in rooms:
        floor_dict.setdefault(room.floor, []).append(room)
    floors = [{'number': floor, 'rooms': rooms} for floor, rooms in sorted(floor_dict.items())]
    return render(request, 'hotel/floor_management.html', {'floors': floors})


@login_required
@role_required(['super_admin', 'owner', 'manager'])
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'hotel/room_form.html', {'form': form, 'title': 'Add Room'})


@login_required
@role_required(['super_admin', 'owner', 'manager'])
def room_edit(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'hotel/room_form.html', {'form': form, 'title': 'Edit Room'})