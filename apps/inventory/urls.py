from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'purchase-orders', views.PurchaseOrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('list/', views.inventory_list, name='inventory_list'),   # <-- this name
]