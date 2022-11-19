from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import datetime


# Create your models here.
# class BaseModel(models.Model):
#     is_deleted = models.BooleanField(default=False)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     deleted_at = models.DateTimeField(null=True)
#
#     class Meta:
#         abstract = True
#
#     def delete(self, using=None, keep_parents=False):
#         self.is_deleted=True
#         self.deleted_at = datetime.now()
#         self.save()
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password):

        if not email:
            raise ValueError('must have user email')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):

        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


# class User(models.Model):
#     email = models.EmailField()
#     password = models.CharField(max_length=20)
#     is_premium = models.BooleanField()
#     # created_at = models.DateTimeField(auto_now_add=True)
#     # deleted_at = models.DateTimeField(null=True, auto_now=True)
#
#     def __str__(self):
#         return self.email


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, default="me")
    description = models.CharField(max_length=50, blank=True)
    social_id = models.CharField(max_length=100, blank=True, unique=True, validators=[MinLengthValidator(4)])
    image = models.ImageField(null=True, blank=True)
    following = models.ManyToManyField('User', related_name='follower')
    is_searchable = models.BooleanField(default=True)
    is_displayed = models.BooleanField(default=True)

    def __str__(self):
        return "keep: " + self.nickname
