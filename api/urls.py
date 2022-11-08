from django.urls import path, include
# from api.views import profile_lists, todo_lists, todo_lists_id
from api.views import *

# user_list = UserViewSet.as_view({
#     'post': 'create',
#     'get': 'list'
# })
urlpatterns = [
    # path('users', profile_lists),
    # path('todolist',todo_lists),
    # path('todolist/<int:pk>/',todo_lists_id),
    path('users', ProfileList.as_view()),
    path('todolist', TodoLists.as_view()),
    path('todolist/<int:pk>', TodoListID.as_view()),
]