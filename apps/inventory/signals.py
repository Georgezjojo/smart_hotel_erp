from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Item
from apps.notifications.models import Notification
from apps.accounts.models import User


@receiver(post_save, sender=Item)
def check_low_stock(sender, instance, **kwargs):
    if instance.quantity <= instance.reorder_level:
        recipients = User.objects.filter(
            role__in=['store_manager', 'super_admin', 'owner', 'manager']
        )

        message = (
            f"Low stock alert: {instance.name} is at {instance.quantity} "
            f"{instance.unit} (reorder level: {instance.reorder_level})."
        )

        for user in recipients:
            # 1. In‑app notification
            Notification.objects.create(
                recipient=user,
                message=message,
                channel='in_app'
            )

            # 2. Send email (if user has an email)
            if user.email:
                send_mail(
                    subject=f'Low Stock Alert – {instance.name}',
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=True,
                )

        # 3. SMS (placeholder – you can integrate a real SMS API later)
        # For now, we just print to the console for demo
        print(f"[SMS] Low stock alert: {instance.name} - {instance.quantity} {instance.unit}")