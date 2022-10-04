from django.db import models
from django.contrib.auth.models import User

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

class Todo(models.Model):
    id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    is_done = models.BooleanField()
    is_stored = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

class Diary(models.Model):
    id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    content = models.TextField()
    bg_color = models.TextField()
    feeling_temp = models.IntegerField()
    emoji = models.CharField()
    is_secret = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()