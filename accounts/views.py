from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from .forms import SignUpForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Follow
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings



class UserListView(ListView):
    model = Profile
    template_name = 'accounts/profile_list.html'
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'


    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

 
        prof = self.object
        user_settings = getattr(prof.user, 'settings', None)

        context['can_view'] = (
            not user_settings or
            user_settings.profile_visibility == 'public' or
            self.request.user == prof.user
        )

      
        if self.request.user.is_authenticated and self.request.user != prof.user:
            context['is_following'] = prof.user in [
                f.following for f in self.request.user.following.all()
            ]
        else:
            context['is_following'] = False

        return context



class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = "accounts/profile_confirm_delete.html"

    def get_object(self):
        return self.request.user.profile

    def test_func(self):
        return self.get_object().user == self.request.user

    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)  
        user.delete()    
        messages.success(request, "Your account and all related data have been deleted.")
        return redirect(reverse_lazy("accounts:login"))


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_form.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse_lazy('accounts:profile_detail', kwargs={'pk': self.object.pk})


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  #not active until verification
        user.save()

        self.send_verification_email(user)
        messages.success(self.request, "Please check your email to verify your account.")
        return redirect('accounts:login')

    def send_verification_email(self, user):
        current_site = get_current_site(self.request)
        subject = "Activate Your Account"
        message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    def get_success_url(self):
        return reverse('posts:post_list')
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')
    http_method_names = ['get', 'post', 'head', 'options']
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.txt'
    html_email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

def profile_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = User.objects.filter(username__icontains=query)
    return render(request, 'accounts/profile_search.html', {'results': results, 'query': query})

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'accounts/profile_detail.html', {'profile': profile})


@login_required
def follow_toggle(request, pk):
    target_user = get_object_or_404(User, pk=pk)

    if request.user == target_user:
        return redirect('accounts:profile_detail', pk=target_user.profile.pk)  # Cannot follow yourself

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:  
        follow.delete()

    return redirect('accounts:profile_detail', pk=target_user.profile.pk)



@login_required
def followers_list(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    followers = user_obj.followers.all()
    return render(request, 'accounts/followers_list.html', {'profile_user': user_obj, 'followers': followers})

@login_required
def following_list(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    following = user_obj.following.all()
    return render(request, 'accounts/following_list.html', {'profile_user': user_obj, 'following': following})


@login_required
def remove_follower(request, pk):
    follower_user = get_object_or_404(User, pk=pk)

    #delete only if actually following me
    Follow.objects.filter(follower=follower_user, following=request.user).delete()

    messages.success(request, f"You have removed {follower_user.username} from your followers.")
    return redirect('accounts:followers_list', pk=request.user.pk)


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        send_mail(
            "Welcome to SocialHub!",
            f"Hi {user.username}, welcome to our platform!",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect('accounts:login')