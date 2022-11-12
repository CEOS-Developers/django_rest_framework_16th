from api import views
from django.urls import path
from api.views import TodoList, TodoDetail

urlpatterns = [
    path('todos/', TodoList.as_view()),
    path('todos/<int:pk>', TodoDetail.as_view()),
]