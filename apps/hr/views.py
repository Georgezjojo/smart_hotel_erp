from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from apps.accounts.permissions import role_required
from .models import Employee, Attendance, Shift          # ✅ added Shift
from rest_framework import viewsets
from .serializers import EmployeeSerializer, AttendanceSerializer, ShiftSerializer


# ═══════════════════════════════════════════════════════════
# API ViewSets
# ═══════════════════════════════════════════════════════════
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


# ═══════════════════════════════════════════════════════════
# HR Dashboard (main landing page)
# ═══════════════════════════════════════════════════════════
@login_required
@role_required(['super_admin', 'owner', 'manager'])
def hr_dashboard(request):
    today = timezone.now().date()

    # Employee stats
    total_employees = Employee.objects.count()
    departments = Employee.objects.values('department').distinct().count()

    # Today's attendance
    attendances = Attendance.objects.select_related('employee__user').filter(date=today)
    present_today = attendances.filter(check_in__isnull=False).count()
    absent_today = total_employees - present_today

    # Recent hires (last 5)
    recent_hires = Employee.objects.select_related('user').order_by('-hire_date')[:5]

    context = {
        'total_employees': total_employees,
        'present_today': present_today,
        'absent_today': absent_today,
        'departments': departments,
        'recent_hires': recent_hires,
        'today': today,
    }
    return render(request, 'hr/hr_dashboard.html', context)


# ═══════════════════════════════════════════════════════════
# Employee Directory
# ═══════════════════════════════════════════════════════════
@login_required
@role_required(['super_admin', 'owner', 'manager'])
def employee_list(request):
    employees = Employee.objects.select_related('user').all()
    total = employees.count()
    departments = employees.values('department').distinct().count()

    context = {
        'employees': employees,
        'total_employees': total,
        'total_departments': departments,
    }
    return render(request, 'hr/employee_list.html', context)


# ═══════════════════════════════════════════════════════════
# Attendance Records (with optional date filter)
# ═══════════════════════════════════════════════════════════
@login_required
@role_required(['super_admin', 'owner', 'manager'])
def attendance_list(request):
    today = timezone.now().date()
    date_str = request.GET.get('date', today.strftime('%Y-%m-%d'))
    try:
        selected_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = today

    attendances = Attendance.objects.select_related('employee__user').filter(date=selected_date)
    present_count = attendances.filter(check_in__isnull=False).count()
    total_employees = Employee.objects.count()
    absent_count = total_employees - present_count

    context = {
        'attendances': attendances,
        'today': selected_date,
        'present_count': present_count,
        'absent_count': absent_count,
        'total_employees': total_employees,
    }
    return render(request, 'hr/attendance.html', context)