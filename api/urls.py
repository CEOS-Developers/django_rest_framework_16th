from django.urls import path
from . import views

urlpatterns = [

    #Todo
    path('todo/', views.todo_list_all, name="todo_all"),
    #'todo/': 모든 user들의 todolist가 다 보이기 때문에 실제로는 쓸 일이 없을 것 같지만.. 모든 데이터 가져오기 연습을 위해 만듦

    path('todo/<int:pk>', views.todo_user, name="todo_user")
]