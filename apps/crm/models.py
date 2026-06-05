from django.db import models
from apps.accounts.models import User

class GuestProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'guest'})
    nationality = models.CharField(max_length=50, blank=True)
    passport_number = models.CharField(max_length=30, blank=True)
    passport_expiry = models.DateField(null=True, blank=True)
    tier = models.CharField(max_length=20, choices=[('regular','Regular'),('vip','VIP'),('blacklisted','Blacklisted')], default='regular')
    loyalty_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name()