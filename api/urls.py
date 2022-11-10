from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [path('todos/', views.todo_list),
               path('todos/<int:id>', views.todo_one)]
