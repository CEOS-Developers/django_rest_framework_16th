from django.urls import path
from .views import *

urlpatterns = [
    path("todo/", TodoListsAPI.as_view()),
    path("todo/<int:pk>/", TodoListAPI.as_view()),
]
