import base64

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10)
    bio = models.TextField(blank=True)
    _profile_img = models.TextField(db_column='profile_img', blank=True)

    def set_profile(self, profile):
        self._profile_img = base64.encodestring(profile)

    def get_profile(self):
        return base64.decodestring(self._profile_img)

    profile_img = property(set_profile, get_profile)


class Friend(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(blank=True)


class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    range = models.IntegerField(default=0)
    is_done = models.BooleanField()
    is_repeat = models.BooleanField()
    cycle = models.IntegerField(default=0)