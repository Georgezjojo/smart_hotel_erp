from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.hotel.models import RoomType, Room
from apps.accounts.models import User
from apps.reservations.models import Reservation


def home(request):
    """Public landing page showing room types."""
    room_types = RoomType.objects.all()
    return render(request, 'home.html', {'room_types': room_types})


def contact(request):
    """Contact us page."""
    return render(request, 'contact.html')


def privacy(request):
    """Privacy policy page."""
    return render(request, 'privacy.html')


def terms(request):
    """Terms of service page."""
    return render(request, 'terms.html')


def search(request):
    """Global search for guests, rooms, and reservations."""
    query = request.GET.get('q', '')
    results = {}
    if query:
        results['guests'] = User.objects.filter(
            first_name__icontains=query
        ) | User.objects.filter(last_name__icontains=query)
        results['rooms'] = Room.objects.filter(room_number__icontains=query)
        results['reservations'] = Reservation.objects.filter(
            guest__email__icontains=query
        )
    return render(request, 'search_results.html', {
        'query': query,
        'results': results,
    })


@login_required
def settings_page(request):
    return render(request, 'settings.html')