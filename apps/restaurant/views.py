from rest_framework import viewsets
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import MenuItem, Table, Order
from .serializers import MenuItemSerializer, TableSerializer, OrderSerializer
from .forms import MenuItemForm
from apps.accounts.permissions import role_required   # centralised decorator


# =================== REST VIEWSETS ===================
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# =================== PUBLIC / INTERNAL MENU ===================
def menu_view(request):
    """Public / internal menu view – switches base template based on user."""
    items = MenuItem.objects.filter(available=True)
    base_template = 'base_public.html'
    if request.user.is_authenticated and request.user.role != 'guest':
        base_template = 'base.html'
    return render(request, 'restaurant/menu.html', {
        'items': items,
        'base_template': base_template,
    })


def table_map(request):
    tables = Table.objects.all()
    return render(request, 'restaurant/table_map.html', {'tables': tables})


def waiter_order(request):
    return render(request, 'restaurant/waiter_order.html')


# =================== STAFF MENU MANAGEMENT ===================
@login_required
@role_required(['super_admin', 'owner', 'manager', 'chef'])
def menu_item_add(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('restaurant_menu')
    else:
        form = MenuItemForm()
    return render(request, 'restaurant/menu_item_form.html', {'form': form})


@login_required
@role_required(['super_admin', 'owner', 'manager', 'chef'])
def menu_item_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('restaurant_menu')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'restaurant/menu_item_form.html', {'form': form})


@login_required
@role_required(['super_admin', 'owner', 'manager', 'chef'])
def menu_item_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Menu item deleted.')
        return redirect('restaurant_menu')
    return render(request, 'restaurant/menu_item_confirm_delete.html', {'item': item})