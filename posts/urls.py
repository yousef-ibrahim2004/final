from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    ToggleLikeView,
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
    post_likes_list,
)

app_name = 'posts'

urlpatterns = [
    path('feed/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/like/', ToggleLikeView.as_view(), name='post_like'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('post/<int:post_pk>/comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('<int:pk>/likes/', post_likes_list, name='post_likes_list'),

    path('post/<int:post_pk>/comment/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
