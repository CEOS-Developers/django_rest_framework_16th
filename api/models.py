from django.db import models

# Create your models here.

class User(models.Model):
    nickname = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to="")
    description = models.CharField(max_length=100)
    show_email = models.BooleanField(default=False)
    show_search = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname

class TodoClass(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=30)
    class_color = models.CharField(max_length=10)
    is_open = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_name


class Todo(models.Model):
    class_id = models.ForeignKey(TodoClass, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="")
    is_finished = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TodoLike(models.Model):
    user_id = models.ForeignKey(User, related_name="TodoLike_User", on_delete=models.CASCADE)
    friend_id = models.ForeignKey(User, related_name="TodoLike_Friend", on_delete=models.CASCADE)
    todo_id = models.ForeignKey(Todo, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.friend_id}, {self.emoji}"


class Diary(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    background_color = models.CharField(max_length=10)
    picture = models.ImageField(upload_to="")
    emoji = models.CharField(max_length=10)
    is_open = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]


class DiaryLike(models.Model):
    diary_id = models.ForeignKey(Diary, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name="DiaryLike_User", on_delete=models.CASCADE)
    friend_id = models.ForeignKey(User, related_name="DiaryLike_Friend", on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.friend_id}, {self.emoji}"