from os import path

from rest_framework.routers import DefaultRouter

from account.views import RegisterAPIView

router = DefaultRouter()
urlpatterns = [
    path('registers/', RegisterAPIView.as_view())
]