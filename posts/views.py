from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from accounts.models import Follow
from django.db.models import Q
from django.http import HttpResponseForbidden


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user

        # Start with public posts
        qs = Post.objects.filter(privacy='public')

        if user.is_authenticated:
            # IDs of users I follow
            i_follow = set(
                Follow.objects.filter(follower=user)
                .values_list('following_id', flat=True)
            )

            # IDs of users who follow me
            follows_me = set(
                Follow.objects.filter(following=user)
                .values_list('follower_id', flat=True)
            )

            # Mutual friends = intersection
            mutual_friends_ids = i_follow & follows_me

            # Own posts (all privacy levels)
            own_posts = Post.objects.filter(author=user)

            # Friends-only posts from mutual friends
            friend_posts = Post.objects.filter(
                privacy='friends',
                author__in=mutual_friends_ids
            )

            # Merge all results
            qs = (qs | own_posts | friend_posts).distinct()

        return qs.order_by('-created_at')

    
    def get_friends(self):
        """
        Placeholder for actual friendship retrieval.
        Replace with your real friendship query if implemented.
        """
        return User.objects.none()


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        user = self.request.user

        if post.privacy == 'public':
            return post

        if not user.is_authenticated:
            raise HttpResponseForbidden("You must be logged in to view this post.")

        # Owner can see their own posts
        if post.author == user:
            return post

        if post.privacy == 'friends':
            # Mutual friendship check
            i_follow = Follow.objects.filter(follower=user, following=post.author).exists()
            follows_me = Follow.objects.filter(follower=post.author, following=user).exists()
            if i_follow and follows_me:
                return post

        # If none of the above, forbid access
        raise HttpResponseForbidden("You do not have permission to view this post.")
    # def get_object(self, queryset=None):
    #     post = super().get_object(queryset)

    #     # Public posts are always visible
    #     if post.privacy == 'public':
    #         return post

    #     # Author can always view their own post
    #     if self.request.user.is_authenticated and self.request.user == post.author:
    #         return post

    #     # Friends-only posts: check friendship
    #     if (
    #         post.privacy == 'friends'
    #         and self.request.user.is_authenticated
    #         and self.request.user in self.get_friends(post.author)
    #     ):
    #         return post

    #     # Otherwise, deny access
    #     raise PermissionDenied("You don't have permission to view this post.")

    def get_friends(self, user):
        """
        Placeholder for actual friendship retrieval.
        Replace with real logic if friendship is implemented.
        """
        return User.objects.none()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_liked'] = self.object.likes.filter(user=self.request.user).exists()
        ctx['comment_form'] = CommentForm()
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:post_list')

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:post_list')

    def test_func(self):
        return self.get_object().author == self.request.user


class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
        return redirect('posts:post_detail', pk=pk)


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect('posts:post_detail', pk=pk)


class CommentDeleteView(LoginRequiredMixin, View):
    template_name = 'posts/comment_confirm_delete.html'

    def get(self, request, post_pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk, post_id=post_pk)
        # Permission check: only comment author or post author
        if comment.author != request.user and comment.post.author != request.user:
            raise PermissionDenied()
        return render(request, self.template_name, {'comment': comment})

    def post(self, request, post_pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk, post_id=post_pk)
        if comment.author == request.user or comment.post.author == request.user:
            comment.delete()
        return redirect('posts:post_detail', pk=post_pk)
    

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # only comment owner can edit

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.post.pk})



def post_likes_list(request, pk):
    post = get_object_or_404(Post, pk=pk)
    likes = post.likes.select_related('user')  # assuming 'likes' is a related_name in Like model
    return render(request, 'posts/post_likes_list.html', {
        'post': post,
        'likes': likes
    })