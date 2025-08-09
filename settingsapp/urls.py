from django.urls import path
from .views import SettingsDetailView, SettingsUpdateView

app_name = 'settingsapp'

urlpatterns = [
    path('', SettingsDetailView.as_view(), name='settings_detail'),
    path('edit/', SettingsUpdateView.as_view(), name='settings_edit'),
]
