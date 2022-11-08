# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Profile, TodoList
from api.serializers import UserSerializer, TodoSerializer

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

class ProfileList(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def get(self,request,format=None):
        profile_lists = Profile.objects.all()
        serializer = UserSerializer(profile_lists, many=True)
        return JsonResponse(serializer.data, safe=False)

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

class TodoLists(APIView):
    def get(self, request, format=None):
        todo_lists = TodoList.objects.all()
        serializer = TodoSerializer(TodoList.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request,format=None):
        data = JSONParser().parse(request)
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def todo_lists_id(request,pk):
#     if request.method == 'GET':
#         todo_list = TodoList.objects.get(id=pk)
#         serializer = TodoSerializer(todo_list)
#
#         return JsonResponse(serializer.data, safe=False)

class TodoListID(APIView):
    def get(self, request, pk):
        todo_list = TodoList.objects.get(id=pk)
        serializer = TodoSerializer(todo_list)

        return JsonResponse(serializer.data, safe=False)