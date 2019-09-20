from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import messages
from .models import Post, Topic
from .forms import AddPostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

# Create your views here.
def posts(request):
    """
    A view which displays all posts in a table on one page
    """
    posts = Post.objects.all()
    posts_total = Post.objects.all().count()

    # Pagination for bugs
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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
    posts = Post.objects.filter(topic=topic)
    # Pagination for bugs
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'posts_by_topic.html', {
        'topic': topic,
        'posts_total': posts_total,
        'posts': posts
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
            post.date_created = timezone.now()
            post.save()
            return redirect(post_detail, post.id)
    else:
        form = AddPostForm(instance=post)
    return render(request, 'add_post.html', {'form': form})

@login_required
def edit_post(request, id):
   post = get_object_or_404(Post, pk=id)
   if request.method == "POST":
       form = AddPostForm(request.POST, request.FILES, instance=post)
       if form.is_valid():
           post = form.save(commit=False)
           post.user = request.user
           post.date_updated = timezone.now()
           post.save()
           return redirect(post_detail, post.id)
   else:
       form = AddPostForm(instance=post)
   return render(request, 'edit_post.html', {'form': form})