from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        qs = Post.objects.filter(privacy='public')

        if self.request.user.is_authenticated:
            own_posts = Post.objects.filter(author=self.request.user)
            friend_posts = Post.objects.filter(
                privacy='friends',
                author__in=self.get_friends()
            )
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

        # Public posts are always visible
        if post.privacy == 'public':
            return post

        # Author can always view their own post
        if self.request.user.is_authenticated and self.request.user == post.author:
            return post

        # Friends-only posts: check friendship
        if (
            post.privacy == 'friends'
            and self.request.user.is_authenticated
            and self.request.user in self.get_friends(post.author)
        ):
            return post

        # Otherwise, deny access
        raise PermissionDenied("You don't have permission to view this post.")

    def get_friends(self, user):
        """
        Placeholder for actual friendship retrieval.
        Replace with real logic if friendship is implemented.
        """
        return User.objects.none()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
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
    def post(self, request, post_pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk, post_id=post_pk)
        if comment.author == request.user:
            comment.delete()
        return redirect('posts:post_detail', pk=post_pk)
