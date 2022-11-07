from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [path('todo/', views.todo_list),
               path('todo/<int:id>', views.todo_one)]
