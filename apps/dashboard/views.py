from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.accounts.permissions import role_required
from apps.reservations.models import Reservation
from apps.hotel.models import Room
from apps.housekeeping.models import Task
from apps.accounting.models import FinancialEntry
from apps.restaurant.models import MenuItem


class DashboardSummaryAPI(APIView):
    """API endpoint that returns current summary data (used for auto‑refresh)."""
    permission_classes = []

    def get(self, request):
        today = timezone.now().date()
        month_start = today.replace(day=1)

        data = {
            'checkins': Reservation.objects.filter(check_in=today, status='checked_in').count(),
            'checkouts': Reservation.objects.filter(check_out=today, status='checked_out').count(),
            'occupancy': round(
                (Room.objects.filter(status='occupied').count() / Room.objects.count() * 100)
                if Room.objects.count() > 0 else 0
            ),
            'revenue': FinancialEntry.objects.filter(
                entry_type='income', date__gte=month_start, date__lte=today
            ).aggregate(total=Sum('amount'))['total'] or 0,
        }
        return Response(data)


@login_required
@role_required(['super_admin', 'owner', 'manager', 'receptionist', 'accountant',
                'store_manager', 'chef', 'waiter', 'housekeeping', 'security'])
def dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # Summary counts
    checkins_today = Reservation.objects.filter(check_in=today, status='checked_in').count()
    checkouts_today = Reservation.objects.filter(check_out=today, status='checked_out').count()
    total_rooms = Room.objects.count()
    occupied_rooms = Room.objects.filter(status='occupied').count()
    occupancy_rate = round((occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0)
    revenue_month = FinancialEntry.objects.filter(
        entry_type='income', date__gte=month_start, date__lte=today
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Active reservations (checked in or arriving within 7 days)
    active_reservations = Reservation.objects.filter(
        status__in=['confirmed', 'checked_in'],
        check_in__lte=today + timedelta(days=7),
        check_out__gte=today
    ).select_related('guest', 'room__room_type').order_by('check_in')[:10]

    # Room timeline (all rooms with current guest)
    rooms = Room.objects.select_related('room_type').all()
    room_timeline = []
    for room in rooms:
        current_res = Reservation.objects.filter(
            room=room,
            check_in__lte=today,
            check_out__gte=today,
            status__in=['confirmed', 'checked_in']
        ).select_related('guest').first()
        room_timeline.append({
            'room': room,
            'current_guest': current_res.guest.get_full_name() if current_res else None
        })

    # Housekeeping counts based on room status
    clean_count = Room.objects.filter(status='available').count()
    dirty_count = Room.objects.filter(status__in=['cleaning', 'maintenance']).count()

    # Recent bookings
    recent_reservations = Reservation.objects.select_related('guest', 'room').order_by('-created_at')[:6]

    # Today's specials – pick 3 random available menu items
    specials = MenuItem.objects.filter(available=True).order_by('?')[:3]

    context = {
        'checkins': checkins_today,
        'checkouts': checkouts_today,
        'occupancy': occupancy_rate,
        'revenue': revenue_month,
        'active_reservations': active_reservations,
        'room_timeline': room_timeline,
        'clean_count': clean_count,
        'dirty_count': dirty_count,
        'recent_reservations': recent_reservations,
        'specials': specials,
    }
    return render(request, 'dashboard/index.html', context)