from django.contrib import admin
from api.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Follower)
admin.site.register(Category)
admin.site.register(Todo)
admin.site.register(Comment)
