from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Q
from django.utils import timezone
from datetime import datetime, timedelta
from apps.reservations.models import Reservation
from apps.billing.models import Invoice, Payment
from apps.inventory.models import Item
from apps.accounting.models import FinancialEntry
from apps.hotel.models import Room
from apps.branches.models import Branch


@login_required
def analytics_dashboard(request):
    today = timezone.now().date()
    start_str = request.GET.get('start_date')
    end_str = request.GET.get('end_date')

    if start_str and end_str:
        try:
            start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = today.replace(day=1)
            end_date = today
    else:
        start_date = today.replace(day=1)
        end_date = today

    # ---------- 1. Profit & Loss ----------
    income_period = FinancialEntry.objects.filter(
        entry_type='income', date__gte=start_date, date__lte=end_date
    ).aggregate(total=Sum('amount'))['total'] or 0
    expenses_period = FinancialEntry.objects.filter(
        entry_type='expense', date__gte=start_date, date__lte=end_date
    ).aggregate(total=Sum('amount'))['total'] or 0
    profit_period = income_period - expenses_period

    room_revenue = Reservation.objects.filter(
        check_in__gte=start_date, check_out__lte=end_date,
        status__in=['checked_in', 'checked_out']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    restaurant_revenue = Invoice.objects.filter(
        issue_date__gte=start_date, issue_date__lte=end_date
    ).aggregate(total=Sum('total'))['total'] or 0
    total_revenue = room_revenue + restaurant_revenue

    # ---------- 2. Balance Sheet (static example) ----------
    total_assets = 1_500_000
    total_liabilities = 120_000
    equity = total_assets - total_liabilities

    # ---------- 3. Cash Flow ----------
    cash_in = Payment.objects.filter(
        timestamp__gte=start_date, timestamp__lte=end_date
    ).aggregate(total=Sum('amount'))['total'] or 0
    cash_out = expenses_period
    net_cash_flow = cash_in - cash_out

    # ---------- 4. Sales Report ----------
    room_sales = Reservation.objects.filter(
        check_in__gte=start_date, check_out__lte=end_date,
        status__in=['checked_in', 'checked_out']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    restaurant_sales = Invoice.objects.filter(
        issue_date__gte=start_date, issue_date__lte=end_date
    ).aggregate(total=Sum('total'))['total'] or 0
    other_income = FinancialEntry.objects.filter(
        entry_type='income', date__gte=start_date, date__lte=end_date
    ).aggregate(total=Sum('amount'))['total'] or 0
    total_sales = room_sales + restaurant_sales + other_income

    # ---------- 5. Inventory Report ----------
    low_stock_items = Item.objects.filter(quantity__lte=F('reorder_level'))

    # ---------- 6. Product Performance (static list) ----------
    product_performance = [
        {'name': 'Fresh Milk', 'sales': 142, 'revenue': 7100},
        {'name': 'White Bread', 'sales': 98, 'revenue': 4900},
        {'name': 'Fruit Juice', 'sales': 24, 'revenue': 1200},
        {'name': 'Eggs', 'sales': 67, 'revenue': 3350},
    ]

    # ---------- 7. Branch Performance ----------
    branches = []
    branch_count = Branch.objects.count()
    for branch in Branch.objects.all():
        branch_revenue = total_revenue / branch_count if branch_count > 0 else 0
        branches.append({
            'name': branch.name,
            'revenue': round(branch_revenue, 2),
            'occupancy': 0,
        })

    # ---------- 8. Expense Report ----------
    expenses_by_category = FinancialEntry.objects.filter(
        entry_type='expense', date__gte=start_date, date__lte=end_date
    ).values('category').annotate(total=Sum('amount')).order_by('-total')

    # ---------- 9. Trend Analysis (6 months) ----------
    trend_labels = []
    trend_revenue = []
    trend_expenses = []
    for i in range(5, -1, -1):
        month = today.replace(day=1) - timedelta(days=i * 30)
        trend_labels.append(month.strftime('%b'))
        inc = FinancialEntry.objects.filter(
            entry_type='income', date__month=month.month, date__year=month.year
        ).aggregate(total=Sum('amount'))['total'] or 0
        exp = FinancialEntry.objects.filter(
            entry_type='expense', date__month=month.month, date__year=month.year
        ).aggregate(total=Sum('amount'))['total'] or 0
        trend_revenue.append(float(inc))
        trend_expenses.append(float(exp))

    # ---------- 10. Customer Report ----------
    top_guests = Reservation.objects.filter(
        check_in__gte=start_date, check_out__lte=end_date
    ).values('guest__first_name', 'guest__last_name', 'guest__email').annotate(
        total_spent=Sum('total_amount')
    ).order_by('-total_spent')[:5]

    # ---------- 11. Tax / VAT Report ----------
    tax_collected = Invoice.objects.filter(
        issue_date__gte=start_date, issue_date__lte=end_date
    ).aggregate(total_tax=Sum('tax'))['total_tax'] or 0

    context = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'income_period': income_period,
        'expenses_period': expenses_period,
        'profit_period': profit_period,
        'total_revenue': total_revenue,
        'room_revenue': room_revenue,
        'restaurant_revenue': restaurant_revenue,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'equity': equity,
        'cash_in': cash_in,
        'cash_out': cash_out,
        'net_cash_flow': net_cash_flow,
        'room_sales': room_sales,
        'restaurant_sales': restaurant_sales,
        'other_income': other_income,
        'total_sales': total_sales,
        'low_stock_items': low_stock_items,
        'product_performance': product_performance,
        'branches': branches,
        'expenses_by_category': expenses_by_category,
        'trend_labels': trend_labels,
        'trend_revenue': trend_revenue,
        'trend_expenses': trend_expenses,
        'top_guests': top_guests,
        'tax_collected': tax_collected,
        'report_generated': timezone.now(),
    }
    return render(request, 'analytics/dashboard.html', context)


@login_required
def report_detail(request):
    report = request.GET.get('report', 'profit_loss')
    today = timezone.now().date()
    start_str = request.GET.get('start_date')
    end_str = request.GET.get('end_date')

    if start_str and end_str:
        try:
            start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = today.replace(day=1)
            end_date = today
    else:
        start_date = today.replace(day=1)
        end_date = today

    context = {
        'report': report,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'generated': timezone.now(),
    }

    if report == 'profit_loss':
        income = FinancialEntry.objects.filter(entry_type='income', date__gte=start_date, date__lte=end_date)
        expenses = FinancialEntry.objects.filter(entry_type='expense', date__gte=start_date, date__lte=end_date)
        total_income = income.aggregate(t=Sum('amount'))['t'] or 0
        total_expenses = expenses.aggregate(t=Sum('amount'))['t'] or 0
        context.update({
            'income_items': income,
            'expense_items': expenses,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'profit': total_income - total_expenses,
        })

    elif report == 'balance_sheet':
        assets = [
            {'name': 'Property & Equipment', 'amount': 1_200_000},
            {'name': 'Cash & Bank', 'amount': 300_000},
        ]
        liabilities = [
            {'name': 'Accounts Payable', 'amount': 50_000},
            {'name': 'Accrued Expenses', 'amount': 70_000},
        ]
        total_assets = sum(a['amount'] for a in assets)
        total_liabilities = sum(l['amount'] for l in liabilities)
        context.update({
            'assets': assets,
            'liabilities': liabilities,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'equity': total_assets - total_liabilities,
        })

    elif report == 'cash_flow':
        cash_in = Payment.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date).aggregate(t=Sum('amount'))['t'] or 0
        cash_out = FinancialEntry.objects.filter(entry_type='expense', date__gte=start_date, date__lte=end_date).aggregate(t=Sum('amount'))['t'] or 0
        context.update({
            'cash_in': cash_in,
            'cash_out': cash_out,
            'net_cash_flow': cash_in - cash_out,
        })

    elif report == 'sales':
        room_sales = Reservation.objects.filter(check_in__gte=start_date, check_out__lte=end_date, status__in=['checked_in','checked_out']).aggregate(t=Sum('total_amount'))['t'] or 0
        restaurant_sales = Invoice.objects.filter(issue_date__gte=start_date, issue_date__lte=end_date).aggregate(t=Sum('total'))['t'] or 0
        other_income = FinancialEntry.objects.filter(entry_type='income', date__gte=start_date, date__lte=end_date).aggregate(t=Sum('amount'))['t'] or 0
        context.update({
            'room_sales': room_sales,
            'restaurant_sales': restaurant_sales,
            'other_income': other_income,
            'total_sales': room_sales + restaurant_sales + other_income,
        })

    elif report == 'inventory':
        low_stock_items = Item.objects.filter(quantity__lte=F('reorder_level'))
        context.update({'low_stock_items': low_stock_items})

    elif report == 'product_performance':
        context.update({
            'products': [
                {'name': 'Fresh Milk', 'sales': 142, 'revenue': 7100},
                {'name': 'White Bread', 'sales': 98, 'revenue': 4900},
                {'name': 'Fruit Juice', 'sales': 24, 'revenue': 1200},
                {'name': 'Eggs', 'sales': 67, 'revenue': 3350},
            ]
        })

    elif report == 'branches':
        branches = []
        branch_count = Branch.objects.count()
        for branch in Branch.objects.all():
            branches.append({
                'name': branch.name,
                'revenue': 0,
                'occupancy': 0,
            })
        context.update({'branches': branches})

    elif report == 'expenses':
        expenses_by_category = FinancialEntry.objects.filter(
            entry_type='expense', date__gte=start_date, date__lte=end_date
        ).values('category').annotate(total=Sum('amount')).order_by('-total')
        total_expenses = sum(e['total'] for e in expenses_by_category)
        context.update({
            'expenses_by_category': expenses_by_category,
            'total_expenses': total_expenses,
        })

    elif report == 'trends':
        trend_labels = []
        trend_revenue = []
        trend_expenses = []
        for i in range(5, -1, -1):
            month = today.replace(day=1) - timedelta(days=i * 30)
            trend_labels.append(month.strftime('%b'))
            inc = FinancialEntry.objects.filter(entry_type='income', date__month=month.month, date__year=month.year).aggregate(t=Sum('amount'))['t'] or 0
            exp = FinancialEntry.objects.filter(entry_type='expense', date__month=month.month, date__year=month.year).aggregate(t=Sum('amount'))['t'] or 0
            trend_revenue.append(float(inc))
            trend_expenses.append(float(exp))
        context.update({
            'trend_labels': trend_labels,
            'trend_revenue': trend_revenue,
            'trend_expenses': trend_expenses,
        })

    elif report == 'customers':
        top_guests = Reservation.objects.filter(
            check_in__gte=start_date, check_out__lte=end_date
        ).values('guest__first_name', 'guest__last_name', 'guest__email').annotate(
            total_spent=Sum('total_amount')
        ).order_by('-total_spent')[:5]
        context.update({'top_guests': top_guests})

    elif report == 'tax':
        tax_collected = Invoice.objects.filter(
            issue_date__gte=start_date, issue_date__lte=end_date
        ).aggregate(total_tax=Sum('tax'))['total_tax'] or 0
        context.update({'tax_collected': tax_collected})

    return render(request, 'analytics/report_detail.html', context)