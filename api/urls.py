# from django.urls import path, include
# from .views import TodoList, TodoDetail
#
# app_name = 'api'
#
# urlpatterns = [path('todos/', TodoList.as_view()),
#                path('todos/<int:id>', TodoDetail.as_view())]

from rest_framework import routers
from .views import TodoViewSet

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)  # register()함으로써 두 개의 url 생성

urlpatterns = router.urls
