from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# 장고에서 primary key 자동으로 만들어줌 (오토 인크레이징으로)

class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # OneToOne 방식 이용
    user_name = models.CharField(max_length=20)
    email = models.EmailField()  # default max : 254
    profile_description = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)  # default max : 200
    is_premium = models.BooleanField(default=False)
    can_search_byemail = models.BooleanField(default=False)
    can_show_todo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name


class Goal(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goal')
    name = models.CharField(max_length=20)
    is_goal_private = models.BooleanField(default=True)
    color = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Todo(models.Model):
    goal_id = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='todo')
    todo_date = models.DateField()
    task = models.CharField(max_length=20)
    time = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    is_kept = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task


class Diary(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary')
    date = models.DateField()
    emoji = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    temperature = models.SmallIntegerField(blank=True, null=True)
    color = models.CharField(max_length=20)
    is_diary_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}의 일기'.format(self.user_id.user_name)


class Follow(models.Model):
    follow_to_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_to_id')
    follow_from_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_from_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} to {}'.format(self.follow_from_id.user_name, self.follow_to_id.user_name)


class DiaryLike(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_like')
    diary_id = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='diary_like')
    emoji = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {} 좋아요'.format(self.user_id.user_name, self.diary_id.date)


class TodoLike(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_like')
    todo_id = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='todo_like')
    like_emoji = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {} 좋아요'.format(self.user_id.user_name, self.todo_id.task)
