from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.accounts.permissions import role_required
from .models import GuestProfile


@login_required
@role_required(['super_admin', 'owner', 'manager', 'receptionist'])
def guest_list(request):
    guests = GuestProfile.objects.select_related('user').all()
    total = guests.count()
    vip_count = guests.filter(tier='vip').count()
    regular_count = guests.filter(tier='regular').count()
    blacklisted = guests.filter(tier='blacklisted').count()

    context = {
        'guests': guests,
        'total_guests': total,
        'vip_count': vip_count,
        'regular_count': regular_count,
        'blacklisted': blacklisted,
    }
    return render(request, 'crm/guest_list.html', context)


@login_required
@role_required(['super_admin', 'owner', 'manager', 'receptionist'])
def guest_profile(request, pk):
    guest = get_object_or_404(GuestProfile.objects.select_related('user'), pk=pk)
    return render(request, 'crm/guest_profile.html', {'guest': guest})