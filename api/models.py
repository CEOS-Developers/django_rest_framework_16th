import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    email = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=10)
    password = models.CharField(max_length=30)
    introduce = models.CharField(max_length=200)
    image = models.ImageField(upload_to="")
    is_public = models.BooleanField(default=False)
    search = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname


class Follow(BaseModel):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)


class Category(BaseModel):
    category_id = models.AutoField(primary_key=True, on_delete=models.CASCADE, related_name='category_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    color = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Todo(BaseModel):
    todo_id = models.AutoField(primary_key=True, on_delete=models.CASCADE, related_name='todo_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_success = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deadline = models.DateField(default=timezone.localtime())
    alarm = models.DateTimeField(null=True)
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content


class Diary(BaseModel):
    diary_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=400)
    emoji = models.CharField(max_length=20)
    public = models.IntegerField(default=0)
    date = models.DateField(default=timezone.localtime())

    def __str__(self):
        return self.content


class DiaryLike(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_like_user')
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='diary_like_diary')
    emoji = models.CharField(max_length=20)

    def __str__(self):
        return 'Diary: {} likes {}'.format(self.user.nickname, self.diary.content)


class TodoLike(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_like_user')
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='todo_like_todo')
    like_emoji = models.CharField(max_length=20)

    def __str__(self):
        return 'Todo: {} likes {}'.format(self.user.nickname, self.todo.content)
