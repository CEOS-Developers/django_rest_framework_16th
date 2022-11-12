from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import  get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import *
from api.serializers import *


class TodoList(APIView):
    def get(self, request):
        todos = Todo.objects.filter(deleted_at=None)
        serializer = TodoSerializer(todos, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class TodoDetail(APIView):
    def get(self, request, pk):
        todo = Todo.objects.filter(todo_id=pk)
        serializer = TodoSerializer(todo, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    def delete(self, request, pk):
        todo = get_object_or_404(Todo, todo_id=pk)
        todo.delete()
        return Response(status=200)

    def patch(self, request, pk):
        todo = get_object_or_404(Todo, todo_id=pk)
        data = JSONParser().parse(request)
        serializer = TodoSerializer(instance=todo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
