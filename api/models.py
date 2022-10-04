from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
# User Model
'''
def create_profile(**kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(user=user)
'''


class Profile(models.Model):
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


class TodoGroup(models.Model):
    user = models.ForeignKey(Profile, related_name='group', db_column='user', on_delete=models.CASCADE)
    group = models.TextField()
    opened = models.TextField(default='all')
    color = models.CharField(max_length=10, default='#000000')

    class Meta:
        db_table = "TodoGroup"

    def __str__(self):
        return self.group


class TodoList(models.Model):
    user = models.ForeignKey(Profile, db_column='user', on_delete=models.CASCADE)
    group = models.ForeignKey(TodoGroup, related_name='list', db_column='group', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    repeated_day = models.IntegerField(default=1111111)
    alarm_time = models.DateTimeField(null=True)
    todo = models.TextField()
    image = models.TextField(null=True)
    status = models.CharField(max_length=10, default='not done')

    class Meta:
        db_table = "TodoList"

    def __str__(self):
        return 'user: {}, todo: {}'.format(self.user, self.todo)


class TodoLikes(models.Model):
    todo_id = models.ForeignKey(TodoList, related_name='todo_likes', db_column='todo_id', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='todo_likes', db_column='user', on_delete=models.CASCADE)
    emoticon = models.ImageField()

    class Meta:
        db_table = "TodoLikes"

    def __str__(self):
        return 'user: {}, emoticon: {}'.format(self.user, self.emoticon)


class Diary(models.Model):
    user = models.ForeignKey(Profile, related_name='diary', db_column='user', on_delete=models.CASCADE)
    date = models.DateField()
    emoji = models.CharField(max_length=20, null=True)
    contents = models.TextField(max_length=500)
    bg_color = models.CharField(max_length=10, default='#FFFFFF')
    temperature = models.IntegerField(default=25)
    image = models.TextField(null=True)
    opened = models.TextField(default='all')

    class Meta:
        db_table = "Diary"

    def __str__(self):
        return self.date


class DiaryLikes(models.Model):
    diary_id = models.ForeignKey(Diary, related_name='diary_likes', db_column='diary_id', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='diary_likes', db_column='user', on_delete=models.CASCADE)
    emoticon = models.ImageField()

    class Meta:
        db_table = "DiaryLikes"

    def __str__(self):
        return 'user: {}, emoticon: {}'.format(self.user, self.emoticon)


class Relation(models.Model):
    follower = models.ForeignKey(Profile, related_name='follower', db_column='follower', on_delete=models.CASCADE)
    followee = models.ForeignKey(Profile, related_name='followee', db_column='followee', on_delete=models.CASCADE)

    class Meta:
        db_table = "Relation"

    def __str__(self):
        return '{} follows {}'.format(self.follower, self.followee)



