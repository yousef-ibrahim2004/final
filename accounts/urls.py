from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView, ProfileDetailView, ProfileUpdateView, UserListView

app_name = 'accounts'

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profiles/', UserListView.as_view(), name='user_list'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]