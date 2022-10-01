from django.db import models
from account.models import Profile, User
from todo.models import Todo
from diary.models import Diary


# Create your models here.


class TodoCheer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='cheer')
    imoji = models.ImageField()


class DiaryCheer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='cheer')
    imoji = models.ImageField()
