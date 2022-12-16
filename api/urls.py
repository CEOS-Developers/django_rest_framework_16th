from rest_framework import routers
from .views import *
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('join/', JoinView.as_view()),
    path('login/', LoginView.as_view()),
    path('test/', Test.as_view())

    # path('token/', TokenObtainPairView.as_view()),
    # path('token/verify', TokenVerifyView.as_view()),
    # path('token/refresh', TokenRefreshView.as_view()),
]

# urlpatterns = [
#     path('todos/', TodoList.as_view()),
#     path('todos/<int:pk>', TodoDetail.as_view()),
# ]
