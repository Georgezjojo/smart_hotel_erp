from django.urls import path
from . import views
urlpatterns = [path('', views.kds_dashboard, name='kds_dashboard')]