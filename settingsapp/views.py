from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import UserSettings
from .forms import SettingsForm

class SettingsDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserSettings
    template_name = 'settingsapp/settings_detail.html'
    context_object_name = 'settings'

    def get_object(self):
        settings, _ = UserSettings.objects.get_or_create(user=self.request.user)
        return settings

    def test_func(self):
        return self.get_object().user == self.request.user


class SettingsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserSettings
    form_class = SettingsForm
    template_name = 'settingsapp/settings_form.html'
    # success_url = reverse_lazy('settingsapp:settings_detail')

    def get_object(self):
        settings, _ = UserSettings.objects.get_or_create(user=self.request.user)
        return settings

    def test_func(self):
        return self.get_object().user == self.request.user
    
    def get_success_url(self):
        # Redirect back to the settings detail page after saving
        return reverse_lazy('settingsapp:settings_detail', kwargs={'pk': self.get_object().pk})
