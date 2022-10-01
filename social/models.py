from django.db import models
from account.models import Profile, User
from todo.models import Todo

# Create your models here.


class Following(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')


class TodoCheer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    imoji = models.ImageField()
