# cars/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Car,User


@receiver(post_save, sender=Car)
def send_email_on_car_status_change(sender, instance, created, **kwargs):
    # Check if the car's status is updated to 'completed' and the car is not newly created
    if not created and instance.status == 'completed':
        # Get the associated client (which is a User with 'client' role)
        try:

            client_user = User.objects.get(id=instance.client_id, role='client')

            # Ensure the client has an email
            if client_user.email:
                send_mail(
                    'Car Status Update: Completed',
                    f'Dear {client_user.username},\n\nYour car with registration number {instance.registration_number} has been completed.',
                    settings.DEFAULT_FROM_EMAIL,
                    [client_user.email],
                    fail_silently=False,
                )
        except User.DoesNotExist:
            pass
