from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/summary/', views.DashboardSummaryAPI.as_view(), name='dashboard_summary_api'),
]