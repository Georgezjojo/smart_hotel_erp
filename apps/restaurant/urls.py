from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'menu', views.MenuItemViewSet)
router.register(r'tables', views.TableViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('menu/', views.menu_view, name='restaurant_menu'),
    path('tables/', views.table_map, name='table_map'),
    path('waiter/', views.waiter_order, name='waiter_order'),
    path('menu/add/', views.menu_item_add, name='menu_item_add'),
    path('menu/add/', views.menu_item_add, name='menu_item_add'),
    path('menu/edit/<int:pk>/', views.menu_item_edit, name='menu_item_edit'),
    path('menu/delete/<int:pk>/', views.menu_item_delete, name='menu_item_delete'),
]