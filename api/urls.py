from django.urls import path
from rest_framework import routers

from api.views import *

router = routers.SimpleRouter()
router.register('todo_classes', TodoClassesViewSet)
router.register('todos', TodoViewSet)

urlpatterns = router.urls + [
    path('signup', SignupView.as_view()),
    path('login', LoginView.as_view())
]