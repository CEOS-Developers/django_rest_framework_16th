from django.urls import path
from .views import *

urlpatterns = [
    path("todo/", TodoListsAPI),
    path("todo/<int:pk>/", TodoListAPI),
]
