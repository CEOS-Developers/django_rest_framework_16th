from api import views
from django.urls import path

urlpatterns = [
    path('todo/', views.todo_list, name="todo_list"),
    path('todo/<int:pk>', views.todo_detail, name="todo_detail"),
]