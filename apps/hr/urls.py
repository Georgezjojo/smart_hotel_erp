from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'shifts', views.ShiftViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('attendance/', views.attendance_list, name='attendance_list'),
]