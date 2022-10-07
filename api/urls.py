from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

# 서로 다른 path 함수를 하나로 묶어 주는 과정
# url prefix, ViewSet
router.register('user', UserViewSet)
router.register('goal', GoalViewSet)
router.register('todo', TodoViewSet)
router.register('like', LikeViewSet)
router.register('follow', FollowViewSet)

urlpatterns = router.urls
