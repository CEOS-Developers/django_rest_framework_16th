from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'privacy', 'color']


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['goal', 'title', 'is_done']
