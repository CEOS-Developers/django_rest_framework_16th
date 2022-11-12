from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.
class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)


class User(BaseModel):
    email = models.EmailField()
    password = models.CharField(max_length=20)
    is_premium = models.BooleanField()

    def __str__(self):
        return self.email


class Profile(BaseModel):
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
