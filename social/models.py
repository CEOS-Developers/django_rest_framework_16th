from django.db import models
from account.models import Profile

# Create your models here.


class Following(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
