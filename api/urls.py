from django.urls import path
from rest_framework import routers
from .views import TodoViewSet
#from . import views
#from api.views import TodoList, TodoItem

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = router.urls

"""
#Urls for Class-Based View
urlpatterns = [
    #Todo
    path('todos/', TodoList.as_view(), name="todo-list"),
    path('todo/<int:pk>/', TodoItem.as_view(), name="todo-item"),
]


#Urls for Fuction-Based View
urlpatterns = [
    #Todo
    path('todos/', views.todo_list, name="todo_list"),
    path('todo/<int:pk>', views.todo_item, name="todo_item"),
]
"""