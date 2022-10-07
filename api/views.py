# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import *

@csrf_exempt
@api_view(['GET','POST'])
def TodoClassesAPI(request):
    if request.method == 'GET':
        todo_classes = TodoClass.objects.all()
        print(todo_classes)
        if len(todo_classes) == 0:
            return Response("Todo Class does not exist")
        serializer = TodoClassesSerializer(todo_classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TodoClassesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['GET'])
def TodoClassAPI(request, id):
    if request.method == 'GET':
        todo_class = get_object_or_404(TodoClass, id=id)
        serializer = TodoClassSerializer(todo_class)
        return Response(serializer.data, status=status.HTTP_200_OK)




@csrf_exempt
@api_view(['GET','POST'])
def TodosAPI(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        if len(todos) == 0:
            return Response("Todo does not exist")
        serializer = TodosSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TodosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['GET'])
def TodoAPI(request, id):
    if request.method == 'GET':
        todo = get_object_or_404(Todo, id=id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)