from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    ToggleLikeView, CommentCreateView, CommentDeleteView
)

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/like/', ToggleLikeView.as_view(), name='post_like'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]