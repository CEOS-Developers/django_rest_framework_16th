from . import views
from django.urls import path

urlpatterns = [
    path('goal', views.GoalView.as_view()),
    path('goal/<int:pk>', views.GoalDetailView.as_view()),
]
