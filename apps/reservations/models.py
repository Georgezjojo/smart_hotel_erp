from django.db import models
from apps.hotel.models import Room
from apps.accounts.models import User

class Reservation(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'guest'})
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('unpaid','Unpaid'),('partial','Partially Paid'),('paid','Fully Paid')], default='unpaid')
    status = models.CharField(max_length=20, choices=[('confirmed','Confirmed'),('checked_in','Checked In'),('checked_out','Checked Out'),('cancelled','Cancelled')], default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest} - {self.room} ({self.check_in} to {self.check_out})"