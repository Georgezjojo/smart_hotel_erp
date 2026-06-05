from django.urls import path
from . import views

urlpatterns = [
    path('', views.guest_list, name='guest_list'),
    path('profile/<int:pk>/', views.guest_profile, name='guest_profile'),
]