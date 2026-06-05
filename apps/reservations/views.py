from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets

from .models import Reservation, Room
from .serializers import ReservationSerializer
from .forms import CheckinForm
from apps.accounts.permissions import role_required


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


@login_required
@role_required(['super_admin', 'owner', 'manager', 'receptionist', 'accountant'])
def reservation_list(request):
    reservations = Reservation.objects.select_related('guest', 'room__room_type').all()
    status = request.GET.get('status')
    date_filter = request.GET.get('date')

    if status:
        reservations = reservations.filter(status=status)
    if date_filter == 'today':
        today = timezone.now().date()
        reservations = reservations.filter(check_in__lte=today, check_out__gte=today)

    return render(request, 'reservations/reservation_list.html', {'reservations': reservations})


@login_required
@role_required(['super_admin', 'owner', 'manager', 'receptionist'])
def add_booking(request):
    if request.method == 'POST':
        room_number = request.POST.get('room')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        try:
            room = Room.objects.get(room_number=room_number)
        except Room.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Room not found'}, status=400)
            messages.error(request, 'Room not found')
            return redirect('add_booking')

        # Placeholder: assign current user as guest (should be improved to find/create guest by email)
        reservation = Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            total_amount=0   # calculate later
        )

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Reservation created successfully!', 'id': reservation.id})
        messages.success(request, 'Reservation created')
        return redirect('reservation_list')

    # GET: provide available rooms for the modal dropdown
    available_rooms = Room.objects.filter(status='available').select_related('room_type')
    return render(request, 'reservations/add_booking_modal.html', {'available_rooms': available_rooms})