from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.

class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=20)
    is_premium = models.BooleanField()


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    social_id = models.CharField(max_length=100, null=True, unique=True, validators=[MinLengthValidator(4)])
    image = models.ImageField(null=True)
    following = models.ManyToManyField('User', related_name='follower')
