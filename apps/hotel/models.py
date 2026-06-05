from django.db import models

class RoomType(models.Model):
    name = models.CharField(max_length=50)
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    max_occupancy = models.IntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('cleaning', 'Cleaning'),
        ('maintenance', 'Maintenance'),
    ]
    room_number = models.CharField(max_length=10, primary_key=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    floor = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)

    def __str__(self):
        return f"{self.room_number} ({self.room_type.name})"