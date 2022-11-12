from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    path('goals/', GoalList.as_view()),
    path('goals/<int:pk>', GoalDetail.as_view()),
]