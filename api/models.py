from django.db import models
# from django.contrib.auth.models import User

# 공통으로 쓰이는 created_at, updated_at, deleted_at model
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(BaseModel):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    email = models.TextField()
    profile_image = models.ImageField()
    can_search_by_email = models.TextField()
    is_shown = models.TextField()

    def __str__(self):
        return self.username

class Goal(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100, default="")
    is_public = models.BooleanField(default=False)
    color = models.CharField(max_length=10, blank=True, default="")

    def __str__(self):
        return self.class_name

class Todo(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    is_done = models.BooleanField(default=False)
    is_stored = models.BooleanField(default=False)
    done_date = models.DateField()

    def __str__(self):
        return self.content

class Diary(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    content = models.TextField()
    bg_color = models.TextField()
    feeling_temp = models.IntegerField()
    emoji = models.CharField(max_length=10)
    is_secret = models.IntegerField()

    def __str__(self):
        return '{}의 일기'.format(self.user.username)