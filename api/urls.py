from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = router.urls

# from api import views
# from django.urls import path
# from api.views import TodoList, TodoDetail
#
# urlpatterns = [
#     path('todos/', TodoList.as_view()),
#     path('todos/<int:pk>', TodoDetail.as_view()),
# ]
