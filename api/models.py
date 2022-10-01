import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.TextField(max_length=10)
    introduce = models.TextField(max_length=200)
    image = models.ImageField(upload_to="")
    is_public = models.BooleanField(default=False)
    search = models.BooleanField(default=False)


# User를 onetoone 방식으로 하면 나머지 클래스에서 foreignkey로 user id를 쓰고 싶을 때 어떻게 해야 하는지 궁금함
class Follower(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Following(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.TextField(max_length=50)
    color = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


class Todo(models.Model):
    todo_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 여기를 CASCADE로 설정하는 것이 맞는지 모르겠다.
    is_success = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deadline = models.DateField(default=timezone.localtime())
    alarm = models.DateTimeField(null=True)
    content = models.CharField(max_length=200)


class Diary(models.Model):
    diary_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=400)
    emoji = models.CharField(max_length=100)
    public = models.IntegerField(default=0)
    deadline = models.DateField(default=timezone.localtime())
