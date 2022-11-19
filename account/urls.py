from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, LoginView, LogoutView, AuthorizationView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('auth/', AuthorizationView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),  # refresh token
]