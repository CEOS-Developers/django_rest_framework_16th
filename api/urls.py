"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('todos/', TodosView.as_view()),
    path('todo/<int:pk>', TodoView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
"""

from rest_framework import routers
from .views import TodoViewSet

router = routers.DefaultRouter()
router.register(r'todo', TodoViewSet)  # register()함으로써 두 개의 url 생성

urlpatterns = router.urls
