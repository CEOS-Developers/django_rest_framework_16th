from django.db import models
from account.models import User
# Create your models here.


class Diary(models.Model):
    PRIVACY_CHOICES = (
        ('나만보기', '나만보기'),
        ('일부공개', '일부공개'),
        ('전체공개', '전체공개')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imoji = models.ImageField()
    date = models.DateField()
    content = models.TextField(max_length=200)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES)
    color = models.CharField(max_length=10, blank=True)
    image = models.ImageField()
    temperature = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "diary: " + self.date

