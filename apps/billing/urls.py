from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
]