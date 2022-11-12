from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import  get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from api.models import *
from api.serializers import *


@csrf_exempt
@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=200)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'DELETE', 'PATCH'])
def todo_detail(request, pk):
    if request.method == 'GET':
        todo = get_object_or_404(Todo, todo_id=pk)
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data, status=200)

    if request.method == 'DELETE':
        todo = Todo.objects.filter(todo_id=pk)
        todo.delete()
        return Response(status=200)

    if request.method == 'PATCH':
        todo = Todo.objects.get(todo_id=pk)
        data = JSONParser().parse(request)
        serializer = TodoSerializer(instance=todo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
