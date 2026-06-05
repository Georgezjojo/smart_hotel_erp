from django.urls import path
from . import views
urlpatterns = [path('demand/', views.DemandPredictionAPI.as_view())]