from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import messages
from .models import Post
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