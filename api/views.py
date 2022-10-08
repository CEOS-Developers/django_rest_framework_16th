from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import *
from api.serializers import *


# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todo_items = Todo.objects.all()
        serializer = TodoSerializer(todo_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
def todo_item(request, pk):

    if request.method == 'GET':
        todo = Todo.objects.filter(id=pk)
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        todo_instance = Todo.objects.filter(id=pk)
        serializer = TodoSerializer(instance=todo_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        todo = Todo.objects.filter(id=pk)
        todo.delete()
        return Response(status=201)

