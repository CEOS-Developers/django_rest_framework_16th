from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import *
from api.serializers import *


# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST'])
def todo_list_all(request):
    if request.method == 'GET':
        todo_items = Todo.objects.all()
        serializer = TodoSerializer(todo_items, many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(['GET','POST'])
def todo_user(request, pk):
    if request.method == 'GET':
        todo_item = Todo.objects.filter(user=pk)
        serializer = TodoSerializer(todo_item, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
