from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),               # Public home page
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('search/', views.search, name='search'),
    path('settings/', views.settings_page, name='settings'),
]