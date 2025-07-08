from django.core.mail import send_mail
from .models import Notification

def send_notification_email(from_mail, to_mail, subject, message):
    # Send the email
    send_mail(
        subject,
        message,
        from_mail,
        [to_mail],
        fail_silently=False,
    )

    # Save to notification table
    Notification.objects.create(
        from_mail=from_mail,
        to_mail=to_mail,
        subject=subject,
        message=message
    )
