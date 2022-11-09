
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'goals', GoalViewSet)
urlpatterns = router.urls

# from . import views
# from django.urls import path
#
# urlpatterns = [
#     path('goals', views.GoalView.as_view()),
#     path('goals/<int:pk>', views.GoalDetailView.as_view()),
# ]
