from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import messages
from .models import Post, Topic
from .forms import AddPostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
def posts(request):
    """
    A view which displays all posts in a table on one page
    """
    posts = Post.objects.all()
    posts_total = Post.objects.all().count()
    return render(request, "posts.html", {
        "posts": posts,
        "posts_total": posts_total
    })

def topics(request):
    topics = Topic.objects.all()
    topics_total = Topic.objects.all().count()
    return render(request, "topics.html", {
        "topics": topics,
        "topics_total": topics_total
    })

def post_detail(request, id):
    """
    A view which displays details for a specific post
    """
    post = get_object_or_404(Post, id=id)
    return render(request, "post_detail.html", {
        'post': post,
    })

def posts_by_topic(request, id):
    topic = get_object_or_404(Topic, id=id)
    posts_total = Post.objects.filter(topic=topic).count()
    return render(request, 'posts_by_topic.html', {
        'topic': topic,
        'posts_total': posts_total,
        'posts': Post.objects.filter(topic=topic)
    })

@login_required
def add_post(request, id=None):
    """
    A view which renders page for add_post form. 
    User must be logged in to access this page. 
    """
    post = get_object_or_404(Post, id=id) if id else None
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(post_detail, post.id)
    else:
        form = AddPostForm(instance=post)
    return render(request, 'add_post.html', {'form': form})