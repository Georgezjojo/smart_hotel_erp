from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation


@receiver(post_save, sender=Reservation)
def update_room_status(sender, instance, **kwargs):
    if instance.status == 'checked_in':
        instance.room.status = 'occupied'
        instance.room.save()
    elif instance.status == 'checked_out':
        instance.room.status = 'cleaning'
        instance.room.save()