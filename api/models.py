from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile/', null=True)
    nickname = models.TextField(max_length=10)
    message = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nickname

class TodoList(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField(max_length=100)
    date_created = models.DateField(auto_now_add=True, verbose_name="Create Date")

    def __str__(self):
        return self.description

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, login_id,  password, **kwargs):
        if not login_id:
            raise ValueError('Users must have an login id')

        user = self.model(
            login_id=login_id,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_id=None, password=None, **extra_fields):
        superuser = self.create_user(
            login_id=login_id,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser
#
# class User(AbstractBaseUser, PermissionsMixin):
#     login_id = models.CharField(max_length=30, unique=True, null=False, blank=False)
#     is_superuser = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'login_id'
#
#     class Meta:
#         db_table = 'user'