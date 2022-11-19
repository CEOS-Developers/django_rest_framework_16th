from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, LoginView, LogoutView, AuthView

urlpatterns = [
    path('register/', RegisterView.as_view()),  # 회원 가입
    path('login/', LoginView.as_view()),  # 로그인
    path('logout/', LogoutView.as_view()),  # 로그 아웃
    path('auth/', AuthView.as_view()),  # 인가 (사용자 확인)
    path('auth/refresh/', TokenRefreshView.as_view()),  # refresh token
]