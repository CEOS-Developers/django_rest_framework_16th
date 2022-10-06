from django.urls import path, include
from .views import getAllTodoList, getTodoList, createTodoList, deleteTodoList, updateTodoList

urlpatterns = [
    path("items/all/", getAllTodoList),
    path("items/<int:pk>/", getTodoList),
    path("items/create/", createTodoList),
    path("items/delete/<int:pk>/", deleteTodoList),
    path("items/update/<int:pk>/", updateTodoList),
]