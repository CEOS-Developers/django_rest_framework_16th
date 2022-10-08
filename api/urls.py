from django.urls import path, include
from api.views import profile_lists, todo_lists, todo_lists_id

# user_list = UserViewSet.as_view({
#     'post': 'create',
#     'get': 'list'
# })
urlpatterns = [
    path('users', profile_lists),
    path('todolist',todo_lists),
    path('todolist/<int:pk>/',todo_lists_id),
]