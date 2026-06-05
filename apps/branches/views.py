from rest_framework import viewsets
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.permissions import role_required
from .models import Branch
from .serializers import BranchSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


@login_required
@role_required(['super_admin', 'owner', 'manager'])
def branch_list(request):
    branches = Branch.objects.all()
    return render(request, 'branches/branch_list.html', {'branches': branches})