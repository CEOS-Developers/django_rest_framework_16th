from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.

class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=20)
    is_premium = models.BooleanField()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, default="me")
    description = models.CharField(max_length=50, blank=True)
    social_id = models.CharField(max_length=100, blank=True, unique=True, validators=[MinLengthValidator(4)])
    image = models.ImageField(null=True, blank=True)
    following = models.ManyToManyField('User', related_name='follower')

    def __str__(self):
        return "keep: " + self.nickname
