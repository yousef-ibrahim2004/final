from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import (
    SignUpView,
    CustomLoginView,
    CustomLogoutView,
    ProfileDetailView,
    ProfileUpdateView,
    UserListView,
    ProfileDeleteView,
    CustomPasswordResetView,
    profile_search,
    profile_detail,
    follow_toggle,
    followers_list,
    following_list,
    remove_follower,
    activate_account,
)


app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),

    #Profiles
    path('profiles/', UserListView.as_view(), name='user_list'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<str:username>/', profile_detail, name='profile_detail_u'),
    path('profile/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile_confirm_delete'),
    path('search/', profile_search, name='profile_search'),

    #follow
    path('profile/<int:pk>/follow-toggle/', follow_toggle, name='follow_toggle'),
    path('profile/<int:pk>/followers/', followers_list, name='followers_list'),
    path('profile/<int:pk>/following/', following_list, name='following_list'),
    path('profile/<int:pk>/remove-follower/', remove_follower, name='remove_follower'),

    #Password Reset
    path(
        'password-reset/',
        CustomPasswordResetView.as_view(template_name='accounts/password_reset.html',
                                        email_template_name='accounts/password_reset_email.txt',
                                        html_email_template_name='accounts/password_reset_email.html',
                                        subject_template_name='accounts/password_reset_subject.txt'),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
                                                    success_url=reverse_lazy('accounts:password_reset_complete')),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]
