from django.db import models
from apps.hotel.models import Room
from apps.accounts.models import User

class Task(models.Model):
    STATUS_CHOICES = [('pending','Pending'), ('in_progress','In Progress'), ('completed','Completed')]
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'housekeeping'})
    task_type = models.CharField(max_length=50, default='cleaning')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)