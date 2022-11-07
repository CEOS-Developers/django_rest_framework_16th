from django.urls import path
from . import views

urlpatterns = [

    #Todo
    path('todo/', views.todo_list, name="todo_list"),
    path('todo/<int:pk>', views.todo_item, name="todo_item"),
]