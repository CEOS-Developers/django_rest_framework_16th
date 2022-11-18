from rest_framework import routers
from .views import *
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register(r'goals', GoalViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view())
]

# from . import views
# from django.urls import path
#
# urlpatterns = [
#     path('goals', views.GoalView.as_view()),
#     path('goals/<int:pk>', views.GoalDetailView.as_view()),
# ]
