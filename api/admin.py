from django.contrib import admin

# Register your models here.
from api.models import TodoClass, Todo, User

admin.site.register(User)
admin.site.register(TodoClass)
admin.site.register(Todo)