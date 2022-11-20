from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

# router
router.register('user', UserViewSet)
router.register('goal', GoalViewSet)
router.register('todo', TodoViewSet)
router.register('like', LikeViewSet)
router.register('follow', FollowViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
]
