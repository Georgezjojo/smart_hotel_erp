from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.accounts.permissions import role_required

from .models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


@login_required
@role_required(['super_admin', 'owner', 'manager', 'accountant'])
def invoice_list(request):
    invoices = Invoice.objects.select_related('reservation__guest', 'reservation__room').all()
    return render(request, 'billing/invoice_list.html', {'invoices': invoices})


@login_required
@role_required(['super_admin', 'owner', 'manager', 'accountant'])
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related(
        'reservation__guest', 'reservation__room__room_type'
    ), pk=pk)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})