from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_intro = models.TextField(blank=True, null=True)  # 길이 제한이 없는 문자열
    profile_image = models.ImageField(blank=True, null=True)


class User(models.Model):
    id = models.BigIntegerField()   # key
    username = models.TextField(max_length=30)
    password = models.TextField(max_length=32)
    email = models.TextField()
    profile_image = models.imageField()
    can_search_by_email = models.TextField()
    is_shown = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(auto_now=True)  # 해당 레코드 갱신시 현재 시간 자동저장
    deleted_at = models.DateTimeField()