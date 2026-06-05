from django.db import models
from apps.reservations.models import Reservation

class KitchenOrder(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
    ]
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)
    room = models.CharField(max_length=20, blank=True)  # e.g., "Room 305"
    table = models.CharField(max_length=20, blank=True)
    items = models.TextField(help_text="JSON list of items")
    special_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    priority = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)