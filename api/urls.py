from api import views
from django.urls import path

urlpatterns = [
    path('todos/', views.todo_list, name="todo_list"),
    path('todos/<int:pk>', views.todo_detail, name="todo_detail"),
]