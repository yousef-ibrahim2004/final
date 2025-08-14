from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags 
from django.conf import settings
from django.contrib.sites.models import Site


@receiver(post_save, sender=User)
def create_profile_and_send_welcome(sender, instance, created, **kwargs):
    if created:
        #create user profile in db
        Profile.objects.create(user=instance) #links profile to user
        
        current_site = Site.objects.get_current()
        protocol = 'https' if settings.SECURE_SSL_REDIRECT else 'http'
        context = {
            'user': instance,
            'domain': current_site.domain,
            'protocol': protocol
        }

        
        subject = 'Welcome to SocialHub 🎉'
        html_message = render_to_string('email/welcome_email.html', context)
        plain_message = strip_tags(html_message)  #converts html to plain


        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            html_message=html_message
        )

#remove any related sett,user,profile from db
@receiver(post_delete, sender=Profile)
def delete_related_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()

#save any related ussser in db
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()