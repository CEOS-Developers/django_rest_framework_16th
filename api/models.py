from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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