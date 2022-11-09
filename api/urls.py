from . import views
from django.urls import path

urlpatterns = [
    path('goals', views.GoalView.as_view()),
    path('goals/<int:pk>', views.GoalDetailView.as_view()),
]
