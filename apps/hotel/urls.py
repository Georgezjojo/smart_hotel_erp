from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'room-types', views.RoomTypeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/public/', views.room_list_public, name='room_list_public'),
    path('room/<str:room_number>/', views.room_detail, name='room_detail'),
    path('floors/', views.floor_list, name='floor_list'),
    path('room/add/', views.room_create, name='room_create'),
    path('room/edit/<str:room_number>/', views.room_edit, name='room_edit'),
]