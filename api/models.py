from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
# User Model


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User, db_column='user', on_delete=models.CASCADE)
    introduction = models.TextField(null=True)
    image = models.TextField(null=True)
    search_yn = models.BooleanField(default=True)
    open_yn = models.BooleanField(default=True)
    start_sunday_yn = models.BooleanField(default=False)
    order_desc_yn = models.BooleanField(default=True)
    input_top_yn = models.BooleanField(default=False)
    check_likes_yn = models.BooleanField(default=True)

    class Meta:
        db_table = "Profile"

    def __str__(self):
        return self.user.username


class TodoGroup(BaseModel):
    user = models.ForeignKey(Profile, related_name='group', db_column='user', on_delete=models.CASCADE)
    group = models.TextField()
    opened = models.TextField(default='all')
    color = models.CharField(max_length=10, default='#000000')

    class Meta:
        db_table = "TodoGroup"

    def __str__(self):
        return self.group


class Todo(BaseModel):
    user = models.ForeignKey(Profile, db_column='user', on_delete=models.CASCADE)
    group = models.ForeignKey(TodoGroup, related_name='list', db_column='group', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    repeated_day = models.IntegerField(default=1111111)
    alarm_time = models.DateTimeField(null=True)
    list = models.TextField()
    image = models.TextField(null=True)
    status = models.CharField(max_length=10, default='not done')

    class Meta:
        db_table = "Todo"

    def __str__(self):
        return 'user: {}, todo: {}'.format(self.user, self.todo)


class TodoLikes(BaseModel):
    todo_id = models.ForeignKey(Todo, related_name='todo_likes', db_column='todo_id', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='todo_likes', db_column='user', on_delete=models.CASCADE)
    emoticon = models.ImageField()

    class Meta:
        db_table = "TodoLikes"

    def __str__(self):
        return 'user: {}, emoticon: {}'.format(self.user, self.emoticon)


class Diary(BaseModel):
    user = models.ForeignKey(Profile, related_name='diary', db_column='user', on_delete=models.CASCADE)
    emoji = models.CharField(max_length=20, null=True)
    contents = models.TextField(max_length=500)
    bg_color = models.CharField(max_length=10, default='#FFFFFF')
    temperature = models.IntegerField(default=25)
    image = models.TextField(null=True)
    opened = models.TextField(default='all')

    class Meta:
        db_table = "Diary"

    def __str__(self):
        return self.created_at


class DiaryLikes(BaseModel):
    diary_id = models.ForeignKey(Diary, related_name='diary_likes', db_column='diary_id', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='diary_likes', db_column='user', on_delete=models.CASCADE)
    emoticon = models.ImageField()

    class Meta:
        db_table = "DiaryLikes"

    def __str__(self):
        return 'user: {}, emoticon: {}'.format(self.user, self.emoticon)


class Relation(BaseModel):
    follower = models.ForeignKey(Profile, related_name='follower', db_column='follower', on_delete=models.CASCADE)
    followee = models.ForeignKey(Profile, related_name='followee', db_column='followee', on_delete=models.CASCADE)

    class Meta:
        db_table = "Relation"

    def __str__(self):
        return '{} follows {}'.format(self.follower, self.followee)



