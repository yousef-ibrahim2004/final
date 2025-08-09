from django import forms
from .models import UserSettings

class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['default_post_privacy', 'email_notifications', 'profile_visibility']
