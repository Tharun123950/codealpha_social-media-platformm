
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import SignUpForm, PostForm, CommentForm, ProfileForm
from .models import Post, Comment, Like, Follow

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def feed(request):
    # Show posts of current user and people they follow
    following_ids = list(Follow.objects.filter(follower=request.user).values_list("following_id", flat=True))
    posts = Post.objects.filter(author_id__in=following_ids + [request.user.id]).order_by("-created_at")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.author = request.user
            p.save()
            return redirect("feed")
    else:
        form = PostForm()
    return render(request, "social/feed.html", {"posts": posts, "form": form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.order_by("created_at")
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.author = request.user
            c.post = post
            c.save()
            return redirect("post_detail", pk=pk)
    else:
        form = CommentForm()
    liked = Like.objects.filter(user=request.user, post=post).exists()
    return render(request, "social/post_detail.html", {"post": post, "comments": comments, "form": form, "liked": liked})

@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect("post_detail", pk=pk)

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    is_self = request.user == user
    posts = user.posts.order_by("-created_at")
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, "social/profile.html", {"profile_user": user, "posts": posts, "is_self": is_self, "is_following": is_following})

@login_required
def follow_toggle(request, username):
    other = get_object_or_404(User, username=username)
    if other == request.user:
        return HttpResponseForbidden("You cannot follow yourself.")
    relation, created = Follow.objects.get_or_create(follower=request.user, following=other)
    if not created:
        relation.delete()
    return redirect("profile", username=username)

@login_required
def edit_profile(request):
    prof = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=prof)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=prof)
    return render(request, "social/edit_profile.html", {"form": form})
