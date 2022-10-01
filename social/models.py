from django.db import models


# Create your models here.


class Following(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='following')
