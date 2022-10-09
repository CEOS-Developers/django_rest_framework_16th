from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # auto_now_add만 추가하면 default 값이 없다고 떠서 default=timezone.now()를 추가하면 둘 중 하나만 쓸 수 있다고 나옵니다. 그래서 우선 null로 해결했는데 이게 맞는지 모르겠습니다ㅠ
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class User(BaseModel):
    email = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=10)
    password = models.CharField(max_length=30)
    introduce = models.CharField(max_length=200)
    image = models.TextField(default=None)
    is_public = models.BooleanField(default=False)
    search = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)


class Category(BaseModel):
    category_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_user')
    title = models.CharField(max_length=50)
    color = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    # is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Todo(BaseModel):
    todo_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_success = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)
    # is_deleted = models.BooleanField(default=False)
    deadline = models.DateField(default=timezone.now())
    alarm = models.DateTimeField(null=True)
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content


class Diary(BaseModel):
    diary_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_user')
    content = models.CharField(max_length=400)
    emoji = models.CharField(max_length=20)
    public = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now())

    def __str__(self):
        return self.content


class TodoLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_todo_user')
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='like_todo')
    emoji = models.CharField(max_length=20)

    def __str__(self):
        return 'Todo: {} likes {}'.format(self.user.nickname, self.todo.content)


class DiaryLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_diary_user')
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='like_diary')
    emoji = models.CharField(max_length=20)

    def __str__(self):
        return 'Diary: {} likes {}'.format(self.user.nickname, self.diary.content)
