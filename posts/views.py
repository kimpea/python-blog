from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import messages
from .models import Post
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
    
    return render(request, "posts.html", {
        "posts": posts,
    })

def post_detail(request, id):
    """
    A view which displays details for a specific post
    """
    post = get_object_or_404(Post, id=id)
    return render(request, "post_detail.html", {
        'post': post,
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