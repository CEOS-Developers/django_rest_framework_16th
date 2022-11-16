from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# 장고에서 primary key 자동으로 만들어줌 (오토 인크레이징으로)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128, null=False)

    def __str__(self):
        return self.username


class Goal(BaseModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='goal_user')
    name = models.CharField(max_length=20)
    is_goal_private = models.BooleanField(default=True)
    color = models.CharField(max_length=20, blank=True, default="#FFF")

    def __str__(self):
        return self.name


class Todo(BaseModel):
    goal = models.ForeignKey("Goal", on_delete=models.CASCADE, related_name='todo_goal')
    todo_date = models.DateField()
    task = models.CharField(max_length=20)
    time = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    is_kept = models.BooleanField(default=False)

    def __str__(self):
        return self.task


class Diary(BaseModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='diary_user')
    date = models.DateField()
    emoji = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    temperature = models.SmallIntegerField(blank=True, null=True)
    color = models.CharField(max_length=20)
    is_diary_private = models.BooleanField(default=False)

    def __str__(self):
        return self.date


class Follow(BaseModel):
    follow_to = models.ForeignKey("User", on_delete=models.CASCADE, related_name='follow_to_user')
    follow_from = models.ForeignKey("User", on_delete=models.CASCADE, related_name='follow_from_user')

    def __str__(self):
        return '{} to {}'.format(self.follow_from.user.username, self.follow_to.user.username)


class DiaryLike(BaseModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='diary_like_user')
    diary = models.ForeignKey("Diary", on_delete=models.CASCADE, related_name='diary_like_diary')
    emoji = models.CharField(max_length=20)

    def __str__(self):
        return '{}: {} 좋아요'.format(self.user.user.username, self.diary.date)


class TodoLike(BaseModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='todo_like_user')
    todo = models.ForeignKey("Todo", on_delete=models.CASCADE, related_name='todo_like_todo')
    like_emoji = models.CharField(max_length=20)

    def __str__(self):
        return '{}: {} 좋아요'.format(self.user.user.username, self.todo.task)
