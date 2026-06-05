from rest_framework import viewsets
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.permissions import role_required

from .models import Item, PurchaseOrder
from .serializers import ItemSerializer, PurchaseOrderSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


@login_required
@role_required(['super_admin', 'owner', 'manager', 'store_manager'])
def inventory_list(request):
    items = Item.objects.all()
    low_stock = [item for item in items if item.quantity <= item.reorder_level]
    return render(request, 'inventory/inventory_list.html', {
        'items': items,
        'low_stock': low_stock
    })