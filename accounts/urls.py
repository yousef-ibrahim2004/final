from django.urls import path
from .views import (
    SignUpView,
    CustomLoginView,
    CustomLogoutView,
    ProfileDetailView,
    ProfileUpdateView,
    UserListView
)
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Profiles
    path('profiles/', UserListView.as_view(), name='user_list'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),

    # Password Reset
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]
