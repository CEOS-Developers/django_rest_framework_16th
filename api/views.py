# views.py
import mixins as mixins
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import viewsets, status, filters, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Profile, TodoList
from api.serializers import UserSerializer, TodoSerializer


User = get_user_model()

# 3주차 과제 코드
# @csrf_exempt
# def profile_lists(request):
    # if request.method == 'GET':
    #     profile_lists = Profile.objects.all()
    #     serializer = UserSerializer(profile_lists, many=True)
    #     return JsonResponse(serializer.data, safe=False)

    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = UserSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def todo_lists(request):
#     if request.method == 'GET':
#         todo_lists = TodoList.objects.all()
#         serializer = TodoSerializer(TodoList.objects.all(), many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = TodoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def todo_lists_id(request,pk):
#     if request.method == 'GET':
#         todo_list = TodoList.objects.get(id=pk)
#         serializer = TodoSerializer(todo_list)
#
#         return JsonResponse(serializer.data, safe=False)

# 4주차 과제 코드
# 1.DRF API View 의 CBV 으로 리팩토링하기
# class ProfileList(APIView):
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self,request,format=None):
#         profile_lists = Profile.objects.all()
#         serializer = UserSerializer(profile_lists, many=True)
#         return Response(serializer.data)
#
# class TodoLists(APIView):
#     def get(self, request, format=None):
#         todo_lists = TodoList.objects.all()
#         serializer = TodoSerializer(TodoList.objects.all(), many=True)
#         return Response(serializer.data)
#
#     def post(self, request,format=None):
#         data = JSONParser().parse(request)
#         serializer = TodoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class TodoListID(APIView):
#     def get(self, request, pk):
#         todo_list = TodoList.objects.get(id=pk)
#         serializer = TodoSerializer(todo_list)
#
#         return Response(serializer.data)

# 2.Viewset으로 리팩토링 하기 & filters
class ProfileFilter(FilterSet):
    user = filters.NumberFilter(field_name="user")
    nickname = filters.CharFilter(field_name="nickname")

    class Meta:
        model = Profile
        fields = ['user','nickname']  # 사용할 모델의 필드


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = Profile.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProfileFilter

class TodoListFilter(FilterSet):
    profile=filters.NumberFilter(field_name="profile")

    class Meta:
        model = TodoList
        fields = ['profile']  # 사용할 모델의 필드

class TodoListViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = TodoList.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TodoListFilter
#
#
# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             # jwt token 접근해주기
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     "token": {
#                         access_token
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
#             res.set_cookie("access", access_token, httponly=True)
#             # res.set_cookie("refresh", refresh_token, httponly=True)
#             return res
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
