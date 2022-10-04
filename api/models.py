from django.db import models
from datetime import datetime
from django.utils import timezone
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


class User(AbstractUser, BaseModel):
    email = models.EmailField(max_length=254, unique=True, verbose_name='사용자 이메일')
    password = models.CharField(max_length=128, null=False, verbose_name='사용자 비밀 번호')
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def __str__(self):
        return self.username


class Goal(BaseModel):
    user = models.ForeignKey('User', related_name='goal', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=30, verbose_name='목표 이름')
    # enum class 생성 필요
    pType = models.TextChoices('pType', 'hide partial full')
    privacy = models.CharField(default='hide', max_length=10)

    def __str__(self):
        return '{} : {}'.format(self.name, self.privacy)


class Todo(BaseModel):
    user = models.ForeignKey(User, related_name='todo', on_delete=models.DO_NOTHING)
    goal = models.ForeignKey(Goal, related_name='todo', on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now, help_text="날짜 및 시간")
    state = models.BooleanField(default=False)
    like_count=models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} : {} : {} : {}'.format(self.user, self.goal, self.content, self.date)


class Like(BaseModel):
    user = models.ForeignKey(User, related_name='like_by', on_delete=models.DO_NOTHING)
    todo = models.ForeignKey(Todo, related_name='like_content', on_delete=models.DO_NOTHING)

    def __str__(self):
        return '{} : {}'.format(self.user, self.todo.content)

# class Following(BaseModel):
#     follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followerUser')
#     following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followingUser')
#
#     def __str__(self):
#         return '{} : {}'.format(self.follower.nickname, self.following.nickname)
