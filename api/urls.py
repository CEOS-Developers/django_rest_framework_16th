from django.urls import path
from . import views

urlpatterns = [
    #Category
    path('category/', views.category_list, name="category"),

    #Todo
    path('todo/', views.todo_list, name="todo"),
    path('todo/<int:pk>', views.todo_user, name="todo_user")
]