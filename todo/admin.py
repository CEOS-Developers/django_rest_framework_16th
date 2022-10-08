from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'privacy', 'color']


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'goal', 'title', 'is_done']
