# views.py

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.utils import json

from .models import User, Todo, Diary, Likes, Follows
from .serializers import TodoSerializer


# 모든 데이터(TodoList)를 가져오는 API
@api_view(['GET'])
def getAllTodoList(request):
    items = TodoSerializer(Todo.objects.all(), many=True)
    return Response(items.data)


# 특정 데이터(TodoList)를 가져오는 API
@api_view(['GET'])
def getTodoList(request, pk):
    item = TodoSerializer(Todo.objects.filter(id=pk))
    return Response(item.data)


# 새로운 데이터(TodoList)를 create하도록 요청하는 API
@api_view(['POST'])
def createTodoList(request):
    req_data = json.loads(request.body)
    result = TodoSerializer.create(TodoSerializer, req_data)
    return Response(result)


# 특정 데이터(TodoList)를 삭제하는 API
@api_view(['DELETE'])
def deleteTodoList(request, pk):
    result = TodoSerializer.delete(TodoSerializer, pk)
    return Response(result)


# 특정 데이터(TodoList)를 업데이트 하는 API
@api_view(['PUT'])
def updateTodoList(request, pk):
    req_data = json.loads(request.body)
    result = TodoSerializer.update(TodoSerializer, pk, req_data)
    return Response(result)
