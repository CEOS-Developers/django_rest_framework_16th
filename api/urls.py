from django.urls import path
from .views import *

urlpatterns = [
    path("todos/", TodoListsAPI.as_view()),
    path("todos/<int:pk>/", TodoListAPI.as_view()),
]
