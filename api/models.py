from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# primary key 자동 생성
class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    # 시간 설정
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()


class User(BaseModel):
    email = models.EmailField(unique=True, verbose_name='사용자 이메일')
    password = models.CharField(null=False, verbose_name='사용자 비밀 번호')
    nickname = models.CharField(max_length=10, unique=True, verbose_name='별명')

    def __str__(self):
        return self.nickname


class Goal(BaseModel):
    user = models.ForeignKey('User', related_name='goal', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name='목표 이름')
    # enum class 생성 필요
    pType = models.TextChoices('pType', 'hide partial full')
    privacy = models.CharField(default='hide', max_length=10)

    def __str__(self):
        return '{} : {}'.format(self.name, self.privacy)


class Todo(BaseModel):
    user = models.ForeignKey(User, related_name='todo', on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, related_name='todo', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    # 시간 입력 어떻게?
    date = models.DateTimeField()
    state = models.BooleanField(default=False)


class Following(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followerUser')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followingUser')

    def __str__(self):
        return '{} : {}'.format(self.follower.nickname, self.following.nickname)
