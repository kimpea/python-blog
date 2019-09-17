"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from .views import posts, topics, post_detail, posts_by_topic, add_post

urlpatterns = [
    path('posts/', posts, name="posts"),
    path('topics/', topics, name="topics"),
    path('post_detail/<int:id>/', post_detail, name="post_detail"),
    path('posts_by_topic/<int:id>/', posts_by_topic, name="posts_by_topic"),
    path('add_post/', add_post, name='add_post'),
]