from django.urls import path, include
from .views import TodoList, TodoDetail

app_name = 'api'

urlpatterns = [path('todos/', TodoList.as_view()),
               path('todos/<int:id>', TodoDetail.as_view())]
