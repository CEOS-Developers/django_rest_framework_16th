from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TodoViewSet
#from . import views
from api.views import *

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterAPIView.as_view()),
    path("auth/", AuthView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
]

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