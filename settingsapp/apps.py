from django.apps import AppConfig


class SettingsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'settingsapp'
    
    def ready(self):
        import settingsapp.signals #noqa
