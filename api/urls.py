from django.urls import path
#from . import views
from api.views import TodoList, TodoItem

urlpatterns = [
    #Todo
    path('todo/', TodoList.as_view(), name="todo-list"),
    path('todo/<int:pk>/', TodoItem.as_view(), name="todo-item"),
]

"""
Urls for Fuction-Based View
#Todo
path('todo/', views.todo_list, name="todo_list"),
path('todo/<int:pk>', views.todo_item, name="todo_item"),
"""