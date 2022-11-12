from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from api.models import *
from api.serializers import *


class TodosView(APIView):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        try:
            lists = Todo.objects.all()
            serializer = TodoSerializer(lists, many=True)
            return Response(serializer.data)
        except AttributeError as e:
            print(e)
            return Response("message: no data")

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        data = request.data
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class TodoView(APIView):
    # noinspection PyMethodMayBeStatic
    def get(self, request, pk):
        try:
            todo = Todo.objects.get(id=pk)
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=201)
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"message: not exist"})
        
    # noinspection PyMethodMayBeStatic
    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(id=pk)
            todo.delete()
            return Response(status=200)
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"message: not exist"})
    
    # noinspection PyMethodMayBeStatic
    def put(self, request, pk):
        try:
            todo = Todo.objects.get(id=pk)
            data = request.data
            serializer = TodoSerializer(todo, data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"message: not exist"})
