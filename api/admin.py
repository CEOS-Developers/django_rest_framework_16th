from django.contrib import admin

# Register your models here.
from .models import Profile, TodoList, User

admin.site.register(Profile)
admin.site.register(TodoList)
# admin.site.register(User)