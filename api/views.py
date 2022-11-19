import os

import environ
import jwt
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import serializers
from .common import *
from .models import *

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters

env = environ.Env(
    DEBUG=(bool, False)
)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class GoalFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    is_goal_private = filters.BooleanFilter(method='private_filter')

    def private_filter(self, queryset, name, value):
        return queryset.filter(is_goal_private=value)

    class Meta:
        model = Goal
        fields = ['name', 'is_goal_private']


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GoalSerializer
    queryset = Goal.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GoalFilter

    # 응답에 필요한 쿼리셋을 가져오기 위해 사용되는 메서드
    def get_queryset(self):
        access_token = self.request.COOKIES['access']
        payload = jwt.decode(access_token, env('SECRET_KEY'), algorithms=['HS256'])
        user_id = payload.get("user_id")
        queryset = super().get_queryset()
        return queryset.filter(user_id=user_id)


class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get("id")
            password = request.data.get("pwd")

            user = User.objects.get(username=username)
            if user.password != password:
                raise
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            res = JsonResponse(custom_response(200, {"token": access_token}), status=200)
            res.set_cookie("access", access_token, httponly=True)
            return res
        except:
            return JsonResponse(custom_response(400), status=400)

# class GoalView(APIView):
#     def get(self, request):
#         user = require_auth(request)
#         if user is None:
#             return JsonResponse(custom_response(401), status=401)
#
#         goals = Goal.objects.filter(user_id=user.id)
#         serializer = serializers.GoalSerializer(goals, many=True)
#         return JsonResponse(custom_response(200, serializer.data), status=200)
#
#     def post(self, request):
#         user = require_auth(request)
#         if user is None:
#             return JsonResponse(custom_response(401), status=401)
#
#         data = JSONParser().parse(request)
#         new_data = {**data, "user": user.id}
#         # ** : spread operator
#         serializer = serializers.GoalSerializer(data=new_data)
#         if not serializer.is_valid():
#             return JsonResponse(custom_response(400, serializer.errors), status=400)
#         serializer.save()
#         return JsonResponse(custom_response(200, serializer.data), status=200)
#
#
# class GoalDetailView(APIView):
#     def get(self, request, pk):
#         # 유저 검증
#         goal = require_auth(request, self, pk)
#         if goal is None:
#             return JsonResponse(custom_response(401), status=401)
#
#         serializer = serializers.GoalSerializer(goal)
#         return JsonResponse(custom_response(200, serializer.data), status=200)
#
#     def delete(self, request, pk):
#         # 유저 검증
#         goal = require_auth(request, self, pk)
#         if goal is None:
#             return JsonResponse(custom_response(401), status=401)
#
#         goal.delete()
#         return JsonResponse(custom_response(204), status=204)
#
#     def put(self, request, pk):
#         # 유저 검증
#         goal = require_auth(request, self, pk)
#         if goal is None:
#             return JsonResponse(custom_response(401), status=401)
#
#         data = JSONParser().parse(request)
#         new_data = {**data, "user": goal.user.id}
#         serializer = serializers.GoalSerializer(goal, data=new_data)
#         if not serializer.is_valid():
#             return JsonResponse(custom_response(400, serializer.errors), status=400)
#         serializer.save()
#         return JsonResponse(custom_response(200, serializer.data), status=200)
