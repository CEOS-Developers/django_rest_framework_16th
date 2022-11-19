import datetime

from django.db import models
from django.conf import settings


def articles_image_path(instance, filename):
    # MEDEIA_ROOT/user_<pk>/ 경로로 <filename> 이름으로 업로드
    return f'user_{instance.pk}/{filename}'


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(blank=True, upload_to=articles_image_path)


class Friend(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_user_id')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')


class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    privacy = models.PositiveIntegerField(default=0)  # 0: 숨기기, 1: 나만 보기, 2: 일부 공개, 3: 전체 공개
    color = models.CharField(max_length=10)  # 16진수 코드로 저장. ex) #ffffff
    order_num = models.PositiveIntegerField(default=0)  # 목표 순서


class ToDo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, default=1)
    content = models.TextField(blank=True)
    date = models.DateField(default=datetime.date.today)
    is_done = models.BooleanField(default=False)
    is_repeat = models.BooleanField(default=False)
    cycle = models.PositiveIntegerField(default=0)
    is_alarm = models.BooleanField(default=False)  # 알람 여부
    is_locker = models.BooleanField(default=False)  # 보관함 여부
    order_num = models.PositiveIntegerField(default=0)  # 할 일 순서


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='like_user_id')
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE, related_name='todo_id')

