from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks_view, name='housekeeping_tasks'),
    path('update-status/<int:task_id>/', views.update_task_status, name='update_task_status'),
]