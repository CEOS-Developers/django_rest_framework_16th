import jwt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django_rest_framework_16th.settings import SECRET_KEY
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, User


# 회원 가입
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save(request.data)
            # jwt token 발급
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(serializer.data, status=status.HTTP_201_CREATED)
            # 쿠키에 넣어서 전달
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            access_token = serializer.validated_data.get('access_token')
            refresh_token = serializer.validated_data.get('refresh_token')
            res = Response(serializer.data, status=status.HTTP_200_OK)
            # 쿠키에 넣어서 전달
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그 아웃
class LogoutView(APIView):
    def post(self, request):
        res = Response(status=status.HTTP_204_NO_CONTENT)
        res.delete_cookie('access')
        res.delete_cookie('refresh')
        return res


# 인가
class AuthView(APIView):
    def get(self, request):
        # access token을 decode해서 유저 id 추출
        access_token = request.COOKIES.get('access')
        if not access_token:
            return Response({"message": "토큰 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            # access token을 decode해서 유저 id 추출
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except jwt.exceptions.InvalidSignatureError:
            # 토큰 유효하지 않음
            return Response({"message": "유효하지 않은 토큰"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            # 토큰 만료 기간 다 됨
            return Response({"message": "토큰 기간 만료"}, status=status.HTTP_401_UNAUTHORIZED)
