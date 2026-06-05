from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api', views.ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', views.reservation_list, name='reservation_list'),
    path('add/', views.add_booking, name='add_booking'),
]