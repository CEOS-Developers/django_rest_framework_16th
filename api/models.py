from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password):

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have an password')

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):

        user = self.create_user(
            email,
            nickname,
            password=password,
        )
        user.is_superuser= True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=30, unique=True)
    nickname = models.CharField(max_length=10)
    password = models.CharField(max_length=30)
    introduce = models.CharField(max_length=200)
    image = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    search = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = "User"

    def __str__(self):
        return self.nickname

    @property
    def is_staff(self):
        return self.is_superuser


# class User(BaseModel):
#     email = models.CharField(max_length=30, unique=True)
#     nickname = models.CharField(max_length=10)
#     password = models.CharField(max_length=30)
#     introduce = models.CharField(max_length=200)
#     image = models.TextField(default=None)
#     is_public = models.BooleanField(default=False)
#     search = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.nickname


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)


class Category(BaseModel):
    category_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_user')
    title = models.CharField(max_length=50)
    color = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Todo(BaseModel):
    todo_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_success = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)
    deadline = models.DateField(default=timezone.now())
    alarm = models.DateTimeField(null=True)
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content


class Diary(BaseModel):
    diary_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_user')
    content = models.CharField(max_length=400)
    emoji = models.CharField(max_length=20)
    public = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now())

    def __str__(self):
        return self.content


class TodoLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_todo_user')
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='like_todo')
    emoji = models.CharField(max_length=20)

    def __str__(self):
        return 'Todo: {} likes {}'.format(self.user.nickname, self.todo.content)


class DiaryLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_diary_user')
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='like_diary')
    emoji = models.CharField(max_length=20)

    def __str__(self):
        return 'Diary: {} likes {}'.format(self.user.nickname, self.diary.content)
