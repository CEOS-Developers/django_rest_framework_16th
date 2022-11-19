from django.db import router
from django.urls import path, include
# from api.views import profile_lists, todo_lists, todo_lists_id
from rest_framework.routers import DefaultRouter
from .views import *
from api.views import *

# user_list = UserViewSet.as_view({
#     'post': 'create',
#     'get': 'list'
# })


# urlpatterns = [
    #3주차 urls
    # path('users', profile_lists),
    # path('todolist',todo_lists),
    # path('todolist/<int:pk>/',todo_lists_id),

    # 4주차 1번 urls
    # path('users', ProfileList.as_view()),
    # path('todolist', TodoLists.as_view()),
    # path('todolist/<int:pk>', TodoListID.as_view()),
# ]

# 4주차 2번 urls
router = DefaultRouter()
router.register('users',ProfileViewSet)
router.register('todolists',TodoListViewSet)

urlpatterns = router.urls
