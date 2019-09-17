from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import auth, messages
from posts.models import Post

# Create your views here.
def index(request):
    """ A view that renders the index page """
    posts = Post.objects.all().order_by('-date_created')[:3]
    return render(request, "index.html", {"posts": posts,})