# Create your views here.
import datetime

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
        todo_classes = TodoClass.objects.filter(deleted_at=None) # filter out soft-deleted Classes
        if len(todo_classes) == 0:
            return Response("Todo Class does not exist", status=status.HTTP_404_NOT_FOUND)
        serializer = TodoClassesSerializer(todo_classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TodoClassesSerializer(data=request.data) # create new todo_class
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['GET', 'PATCH'])
def TodoClassAPI(request, id):
    if request.method == 'GET':
        todo_class = get_object_or_404(TodoClass, id=id)
        if(todo_class.deleted_at != None): # check if the class had been soft-deleted
            return Response("Todo Class does not exist", status=status.HTTP_404_NOT_FOUND)
        serializer = TodoClassSerializer(todo_class)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        print(request.data)
        todo_class = get_object_or_404(TodoClass, id=id)
        if(request.data != {}):
            todo_class.class_name = request.data['class_name']
            todo_class.class_color = request.data['class_color']
            todo_class.is_open = request.data['is_open']
        else:
            todo_class.deleted_at = datetime.datetime.now() # soft-delete todo_class
        todo_class.save()
        serializer = TodoClassSerializer(todo_class)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



@csrf_exempt
@api_view(['GET','POST'])
def TodosAPI(request):
    if request.method == 'GET':
        todos = Todo.objects.filter(deleted_at=None) # filter out soft-deleted todos
        if len(todos) == 0:
            return Response("Todo does not exist", status=status.HTTP_404_NOT_FOUND)
        serializer = TodosSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TodosSerializer(data=request.data) # create new todo
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['GET', 'PATCH'])
def TodoAPI(request, id):
    if request.method == 'GET':
        todo = get_object_or_404(Todo, id=id)
        if(todo.deleted_at != None): # check if the todo had been soft-deleted
            return Response("Todo does not exist", status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        print(request.data)
        todo = get_object_or_404(Todo, id=id)
        if(request.data != {}):
            todo.title = request.data['title']
            todo.image = request.data['image']
            todo.is_finished = request.data['is_finished']
            todo.is_default = request.data['is_default']
        else:
            todo.deleted_at = datetime.datetime.now() # soft-delete todo
        todo.save()
        serializer = TodosSerializer(todo)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
