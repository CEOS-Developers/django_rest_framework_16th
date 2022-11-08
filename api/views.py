# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Profile, TodoList
from api.serializers import UserSerializer, TodoSerializer

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

# 2.Viewset으로 리팩토링 하기
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = Profile.objects.all()

class TodoListViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = TodoList.objects.all()