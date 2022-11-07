from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    path('goals/', goal_list),
    path('goals/<int:pk>', goal_detail),
]