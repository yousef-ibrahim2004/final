from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('private', 'Private'),
    ]

    PROFILE_VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    default_post_privacy = models.CharField(
        max_length=10,
        choices=PRIVACY_CHOICES,
        default='public',
        help_text="Default privacy level for new posts."
    )
    email_notifications = models.BooleanField(
        default=True,
        help_text="Receive email notifications for key actions."
    )
    profile_visibility = models.CharField(
        max_length=10,
        choices=PROFILE_VISIBILITY_CHOICES,
        default='public',
        help_text="Who can view your profile."
    )

    def __str__(self):
        return f"Settings for {self.user.username}"
