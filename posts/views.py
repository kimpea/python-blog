from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import messages
from .models import Post, Topic, PostComment
from .forms import AddPostForm, PostCommentForm
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
    topics = Topic.objects.all()
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
        "posts_total": posts_total,
        "topics": topics
    })

def post_detail(request, id):
    """
    A view which displays details for a specific post
    """
    post = get_object_or_404(Post, id=id)
    topics = Topic.objects.all()
    comments = PostComment.objects.filter(post=id).order_by('date_created')
    comments_count = comments.count()
    comment_form = PostCommentForm()
    return render(request, "post_detail.html", {
        'post': post,
        'comment_form': comment_form, 
        'comments': comments,
        'comments_count': comments_count,
        'topics': topics
    })

def posts_by_topic(request, id):
    topic = get_object_or_404(Topic, id=id)
    topics = Topic.objects.all()
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
        'topics': topics,
        'posts_total': posts_total,
        'posts': posts
    })

@login_required
def add_post(request, id=None):
    """
    A view which renders page for add_post form. 
    User must be logged in to access this page. 
    """
    topics = Topic.objects.all()
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
    return render(request, 'add_post.html', {
        'form': form,
        'topics': topics
    })

@login_required
def edit_post(request, id):
    topics = Topic.objects.all()
    post = get_object_or_404(Post, id=id)

    if post.user.id != request.user.id:
        messages.error(request, "You cannot edit someone else's post!")
        return redirect('post_detail', post.id)

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
    return render(request, 'edit_post.html', {
       'form': form,
       'topics': topics
    })

@login_required
def post_comment(request, id=id):
    """ Saves a posted comment """
    post = get_object_or_404(Post, id=id)
    comment_form = PostCommentForm(request.POST, request.FILES)
    if comment_form.is_valid():
        instance = comment_form.save(commit=False)
        instance.user = request.user
        instance.post = post
        comment_form.save()
    return redirect(post_detail, id)