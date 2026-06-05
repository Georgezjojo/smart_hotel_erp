from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('owner', 'Hotel Owner'),
        ('manager', 'General Manager'),
        ('receptionist', 'Receptionist'),
        ('accountant', 'Accountant'),
        ('store_manager', 'Store Manager'),
        ('chef', 'Chef'),
        ('waiter', 'Waiter'),
        ('housekeeping', 'Housekeeping'),
        ('security', 'Security'),
        ('guest', 'Guest'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email_verified = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=False)

    # Additional profile fields
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    # Make email unique (required when USERNAME_FIELD = 'email')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def get_initials(self):
        if self.first_name and self.last_name:
            return (self.first_name[0] + self.last_name[0]).upper()
        elif self.email:
            return self.email[:2].upper()
        return '??'

    def __str__(self):
        return self.get_full_name() or self.email