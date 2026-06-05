from django.db import models
from apps.accounts.models import User

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(max_length=20, choices=[('in_app', 'In-App'), ('email', 'Email'), ('sms', 'SMS')], default='in_app')

    def __str__(self):
        return f"To {self.recipient}: {self.message[:50]}..."