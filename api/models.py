from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now
        self.save(update_fields=['deleted_at'])

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, id, nickname, email, password, **extra_fields):
        if not id:
            raise ValueError('Users require an id field')
        if not nickname:
            raise ValueError('Users require a nickname field')
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(id=id, nickname=nickname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, id, nickname, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(id, nickname, email, password, **extra_fields)

    def create_superuser(self, id, nickname, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(id, nickname, email, password, **extra_fields)


class User(AbstractBaseUser, BaseModel):
    id = models.CharField(max_length=20, primary_key=True)
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'nickname', ]

    def __str__(self):
        return self.nickname


class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)


class Category(BaseModel):
    category_name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.category_name


class Todo(BaseModel):
    DISCLOSURE_CHOICES = {
        ('private', 'Private'),
        ('onlyFriends', 'Only Friends'),
        ('public', 'Public'),
    }
    todo_name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    disclosure_choice = models.CharField(default='public', max_length=30, choices=DISCLOSURE_CHOICES)
    date = models.DateTimeField(default=now)
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return self.todo_name


class Comment(BaseModel):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=1)
    comment = models.CharField(max_length=200)