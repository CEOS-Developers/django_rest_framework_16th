from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

class Category(models.Model):
    category_name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.category_name


class Todo(models.Model):
    DISCLOSURE_CHOICES = {
        ('private', 'Private'),
        ('onlyFriends', 'Only Friends'),
        ('public', 'Public'),
    }
    todo_name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    disclosure_choice = models.CharField(default='public', max_length=30, choices=DISCLOSURE_CHOICES)
    date = models.DateTimeField(default=now)
    def __str__(self):
        return self.todo_name


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=1)
    comment = models.CharField(max_length=200)