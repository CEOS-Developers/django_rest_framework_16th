"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('todos/', TodosView.as_view()),
    path('todo/<int:pk>', TodoView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
"""

from django.urls import path
from rest_framework import routers
from .views import TodoViewSet, LoginView, JoinView
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register(r'todo', TodoViewSet)

urlpatterns = [
    path('join/', JoinView.as_view()),
    path('login/', LoginView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
]

urlpatterns += router.urls
