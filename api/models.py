from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import datetime

# Create your models here.
# User Model


STATUS_CHOICES = (

    (0, 'Not Done'),

    (1, 'Done'),

    (2, 'Not to disclose')

)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password):

        if not email:
            raise ValueError('Email cannot be null')

        if not password:
            raise ValueError('Password cannot be null')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):

        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=20, default='me')
    image = models.TextField(null=True)
    search_yn = models.BooleanField(default=True)
    open_yn = models.BooleanField(default=True)
    start_sunday_yn = models.BooleanField(default=False)
    order_desc_yn = models.BooleanField(default=True)
    input_top_yn = models.BooleanField(default=False)
    check_likes_yn = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = "MyUser"

    def __str__(self):
        return self.email

    def get_nickname(self):
        return self.nickname

    def get_full_name(self):
        pass

    def get_short_name(self):
        pass

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value

# class Profile(BaseModel):
#     user = models.OneToOneField(User, db_column='user', on_delete=models.CASCADE)
#     introduction = models.TextField(null=True)
#     image = models.TextField(null=True)
#     search_yn = models.BooleanField(default=True)
#     open_yn = models.BooleanField(default=True)
#     start_sunday_yn = models.BooleanField(default=False)
#     order_desc_yn = models.BooleanField(default=True)
#     input_top_yn = models.BooleanField(default=False)
#     check_likes_yn = models.BooleanField(default=True)
#
#     class Meta:
#         db_table = "Profile"
#
#     def __str__(self):
#         return self.user.username


class TodoGroup(BaseModel):
    user = models.ForeignKey(MyUser, related_name='group', db_column='user', on_delete=models.CASCADE)
    group = models.TextField()
    opened = models.TextField(default='all')
    color = models.CharField(max_length=10, default='#000000')

    class Meta:
        db_table = "TodoGroup"

    def __str__(self):
        return self.group


class Todo(BaseModel):
    user = models.ForeignKey(MyUser, db_column='user', on_delete=models.CASCADE)
    group = models.ForeignKey(TodoGroup, related_name='todo', db_column='group', on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    repeated_day = models.IntegerField(default=1111111)
    alarm_time = models.DateTimeField(null=True)
    contents = models.TextField()
    image = models.TextField(null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)

    class Meta:
        db_table = "Todo"

    def __str__(self):
        return 'user: {}, todo: {}'.format(self.user, self.todo)


class TodoLikes(BaseModel):
    todo_id = models.ForeignKey(Todo, related_name='todo_likes', db_column='todo_id', on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, related_name='todo_likes', db_column='user', on_delete=models.CASCADE)
    emoticon = models.ImageField()

    class Meta:
        db_table = "TodoLikes"

    def __str__(self):
        return 'user: {}, emoticon: {}'.format(self.user, self.emoticon)


class Diary(BaseModel):
    user = models.ForeignKey(MyUser, related_name='diary', db_column='user', on_delete=models.CASCADE)
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
    user = models.ForeignKey(MyUser, related_name='diary_likes', db_column='user', on_delete=models.CASCADE)
    emoticon = models.ImageField()

    class Meta:
        db_table = "DiaryLikes"

    def __str__(self):
        return 'user: {}, emoticon: {}'.format(self.user, self.emoticon)


class Relation(BaseModel):
    follower = models.ForeignKey(MyUser, related_name='follower', db_column='follower', on_delete=models.CASCADE)
    followee = models.ForeignKey(MyUser, related_name='followee', db_column='followee', on_delete=models.CASCADE)

    class Meta:
        db_table = "Relation"

    def __str__(self):
        return '{} follows {}'.format(self.follower, self.followee)
