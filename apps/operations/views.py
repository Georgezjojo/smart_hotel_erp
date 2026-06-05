from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.permissions import role_required


@login_required
@role_required(['super_admin', 'owner', 'manager', 'receptionist', 'accountant',
                'store_manager', 'chef', 'waiter', 'housekeeping', 'security'])
def chat_view(request):
    return render(request, 'operations/chat.html')