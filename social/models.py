from django.db import models
from account.models import User, BaseModel
from todo.models import Todo
from diary.models import Diary


# Create your models here.


class TodoCheer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='cheer')
    imoji = models.ImageField()

    def __str__(self):
        return "todo cheer: " + self.user.email


class DiaryCheer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='cheer')
    imoji = models.ImageField()

    def __str__(self):
        return "diary cheer: " + self.user.email
