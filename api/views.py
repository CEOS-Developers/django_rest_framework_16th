from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import *
from api.serializers import *


@csrf_exempt
@api_view(['GET', 'POST'])
def todos(request):
    if request.method == 'GET':
        lists = Todo.objects.all()
        serializer = TodoSerializer(lists, many=True)
        return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'DELETE', 'PUT'])
def todo(request, pk):
    if request.method == 'GET':
        todo = Todo.objects.get(id=pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=201)

    elif request.method == 'DELETE':
        todo = Todo.objects.get(id=pk)
        todo.delete()
        return JsonResponse(status=200)

    elif request.method == 'PUT':
        todo = Todo.objects.get(id=pk)
        data = JSONParser().parse(request)

        serializer = TodoSerializer(todo, data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)