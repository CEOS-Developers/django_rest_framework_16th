# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .serializers import *


@api_view(['GET', 'POST'])
def TodoListsAPI(request):
    if request.method == 'GET':
        items = TodoSerializer(Todo.objects.all(), many=True)
        return Response(items.data)

    elif request.method == 'POST':
        req_data = JSONParser().parse(request)
        result = TodoSerializer.create(TodoSerializer, req_data)
        return Response(result)


# 특정 데이터(TodoList)를 가져오는 API
@api_view(['GET','DELETE', 'PUT'])
def TodoListAPI(request, pk):
    if request.method == 'GET':
        item = TodoSerializer(Todo.objects.get(id=pk))
        return Response(item.data)

    elif request.method == 'DELETE':
        result = TodoSerializer.delete(TodoSerializer, pk)
        return Response(result)

    elif request.method == 'PUT':
        req_data = JSONParser().parse(request)
        result = TodoSerializer.update(TodoSerializer, pk, req_data)
        return Response(result)

