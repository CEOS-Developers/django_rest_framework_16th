from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(models.Model):
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=25, unique=True)
    web_id = models.CharField(max_length=15, null=True)
    web_pw = models.CharField(max_length=25)
    intro_text = models.TextField(null=True)

    def __str__(self):
        return self.name


class Todo(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='user info')
    contents = models.TextField()
    date = models.DateField()
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.contents

class Diary(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='user info')
    emoji = models.CharField(max_length=15)
    mood_temperature = models.IntegerField(default=25)
    date = models.DateField()
    contents = models.TextField()
    background_color = models.CharField(max_length=15)
    private = models.BooleanField(default=False)
    image = models.ImageField(null=True)

    def __str__(self):
        return '{} 일기'.format(self.user.name)


class Likes(models.Model):
    # 좋아요를 누른 유저
    click_user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='user info')
    todo = models.ManyToManyField(Todo)
    diary = models.ManyToManyField(Diary)

    def __str__(self):
        return '{}가 {}의 글을 좋아합니다.'.format(self.click_user.name, self.todo.user.name)


class Follows(models.Model):
    # 팔로우를 건 유저
    click_user = models.ManyToManyField(User, related_name='click_user')
    # 팔로우 타겟
    target = models.ManyToManyField(User, related_name='target_user')

    def __str__(self):
        return '{}가 {}를 팔로우합니다.'.format(self.click_user.name, self.target.name)