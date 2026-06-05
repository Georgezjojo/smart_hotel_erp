from django.db import models
from apps.accounts.models import User

class DigitalKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('hotel.Room', on_delete=models.CASCADE)
    qr_code_data = models.CharField(max_length=200, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)