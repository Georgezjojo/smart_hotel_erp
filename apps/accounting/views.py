from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from apps.accounts.permissions import role_required
from .models import FinancialEntry
import calendar


@login_required
@role_required(['super_admin', 'owner', 'manager', 'accountant'])
def profit_loss(request):
    today = timezone.now().date()
    year = today.year

    # Monthly breakdown for the current year
    monthly_labels = []
    monthly_income = []
    monthly_expenses = []
    for month in range(1, 13):
        month_name = calendar.month_abbr[month]
        monthly_labels.append(month_name)
        inc = FinancialEntry.objects.filter(
            entry_type='income',
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0
        exp = FinancialEntry.objects.filter(
            entry_type='expense',
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0
        monthly_income.append(float(inc))
        monthly_expenses.append(float(exp))

    # Yearly totals
    total_income = sum(monthly_income)
    total_expenses = sum(monthly_expenses)
    profit = total_income - total_expenses

    # Recent entries
    entries = FinancialEntry.objects.order_by('-date')[:20]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'profit': profit,
        'entries': entries,
        'monthly_labels': monthly_labels,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'year': year,
    }
    return render(request, 'accounting/profit_loss.html', context)


@login_required
@role_required(['super_admin', 'owner', 'manager', 'accountant'])
def add_financial_entry(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        entry_type = request.POST.get('entry_type')
        category = request.POST.get('category', '')

        if date and description and amount and entry_type:
            FinancialEntry.objects.create(
                date=date,
                description=description,
                amount=amount,
                entry_type=entry_type,
                category=category
            )
            messages.success(request, 'Financial entry added successfully.')
            return redirect('profit_loss')
        else:
            messages.error(request, 'Please fill all required fields.')

    return render(request, 'accounting/invoice.html')