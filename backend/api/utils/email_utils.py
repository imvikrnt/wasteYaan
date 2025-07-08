from django.core.mail import send_mail
from django.conf import settings


def send_user_registration_email(to_email, name, user_id):
    subject = 'Welcome to WasteYaan - Your User ID'
    message = f"""
Hi {name},

Thank you for registering with WasteYaan 🚀

Your User ID is: {user_id}

Please keep this ID safe. You’ll need it to log in.

Regards,  
Team WasteYaan
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )
