from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.permissions import role_required
from .models import KitchenOrder


@login_required
@role_required(['super_admin', 'owner', 'manager', 'chef'])
def kds_dashboard(request):
    orders = KitchenOrder.objects.filter(
        status__in=['pending', 'preparing']
    ).order_by('-priority', 'created_at')
    return render(request, 'kitchen_display/kds_dashboard.html', {'orders': orders})