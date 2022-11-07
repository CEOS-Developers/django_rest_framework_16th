from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Profile)
admin.site.register(Goal)
admin.site.register(Todo)
admin.site.register(Diary)