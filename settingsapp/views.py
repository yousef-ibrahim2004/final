from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserSettings
from .forms import SettingsForm
from django.urls import reverse_lazy

class SettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = UserSettings
    form_class = SettingsForm
    template_name = 'settingsapp/settings_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def get_object(self):
        obj, created = UserSettings.objects.get_or_create(user=self.request.user)
        return obj