# from django.urls import path
from rest_framework import routers
from .views import *

# # CBV용 url
# urlpatterns = [
#     path("todos/", TodoListsAPI.as_view()),
#     path("todos/<int:pk>/", TodoListAPI.as_view()),
# ]

router = routers.DefaultRouter()
router.register(r'todos', TodoListViewSet, basename='todo')

urlpatterns = router.urls