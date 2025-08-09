from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@receiver(post_save, sender=User)
def create_profile_and_send_welcome(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # send welcome email
        subject = 'Welcome to SocialHub'
        html_message = render_to_string('email/welcome_email.html', {'user': instance})
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [instance.email], html_message=html_message)