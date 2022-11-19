from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


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


# 로그아웃
class LogoutView(APIView):
    def post(self, request):
        res = Response(status=status.HTTP_204_NO_CONTENT)
        res.delete_cookie('access')
        res.delete_cookie('refresh')
        return res


# 인가
class AuthorizationView(APIView):
    def get(self, request):
        res = JWTAuthentication().authenticate(request)
        user, token = res

        if not user:
            return Response({"접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

