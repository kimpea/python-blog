from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=254, default=None)
    body = models.TextField()
    topic = models.ForeignKey(Topic, default="None", on_delete=models.SET_DEFAULT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, default="", on_delete=models.CASCADE)

    def __str__(self):
        return self.title