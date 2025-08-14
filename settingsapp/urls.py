from django.urls import path
from .views import SettingsDetailView, SettingsUpdateView

app_name = 'settingsapp'

urlpatterns = [
    path('<int:pk>/', SettingsDetailView.as_view(), name='settings_detail'),
    path('<int:pk>/edit/', SettingsUpdateView.as_view(), name='settings_edit'),
]
