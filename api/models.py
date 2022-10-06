from django.db import models

# Create your models here.

class User(models.Model):
    nickname = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=50, blank=True)
    profile_image = models.TextField()
    description = models.CharField(max_length=100)
    show_email = models.BooleanField(default=False)
    show_search = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True)

    def __str__(self):
        return self.nickname

class TodoClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=30)
    class_color = models.CharField(max_length=10)
    is_open = models.IntegerField(default=0) #0:나만보기 1:친구공개 2:전체공개
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True)

    def __str__(self):
        return self.class_name


class Todo(models.Model):
    todo_class = models.ForeignKey(TodoClass, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.TextField()
    is_finished = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title


class TodoLike(models.Model):
    user_from = models.ForeignKey(User, related_name="TodoLike_From", on_delete=models.CASCADE, default='')
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.user_from}, {self.emoji}"


class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    background_color = models.CharField(max_length=10)
    picture = models.TextField()
    emoji = models.CharField(max_length=10)
    is_open = models.IntegerField(default=0) #0:나만보기 1:친구공개 2:전체공개
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True)

    def __str__(self):
        return self.content[:20]


class DiaryLike(models.Model):
    user_from = models.ForeignKey(User, related_name="DiaryLike_From", on_delete=models.CASCADE, default='')
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.user_from}, {self.emoji}"