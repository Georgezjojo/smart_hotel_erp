from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'branches', views.BranchViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('list/', views.branch_list, name='branch_list'),
]