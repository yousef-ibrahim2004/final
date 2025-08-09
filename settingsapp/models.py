from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('private', 'Private'),
    ]
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    default_post_privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    email_notifications = models.BooleanField(default=True)
    profile_visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')

    def __str__(self):
        return f"Settings for {self.user.username}"
