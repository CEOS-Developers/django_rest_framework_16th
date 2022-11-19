from django.urls import path, include
from .views import *
from rest_framework import routers

app_name = 'todo'

router = routers.DefaultRouter()
router.register('goals', GoalViewSet)

urlpatterns = [
    # path('goals/', GoalList.as_view()),
    # path('goals/<int:pk>', GoalDetail.as_view()),
    path('', include(router.urls)),
]