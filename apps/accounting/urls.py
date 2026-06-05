from django.urls import path
from . import views

urlpatterns = [
    path('', views.profit_loss, name='profit_loss'),
    path('add/', views.add_financial_entry, name='add_financial_entry'),
]