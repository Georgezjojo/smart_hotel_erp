from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_dashboard, name='analytics'),
    path('details/', views.report_detail, name='report_detail'),
]