# Create your views here.
import datetime

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import *


class TodoClassesViewSet(viewsets.ModelViewSet):
    queryset = TodoClass.objects.all()
    serializer_class = TodoClassSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

#
# class TodosAPI(APIView):
#     def get(self, request):
#         todos = Todo.objects.filter(deleted_at=None)  # filter out soft-deleted todos
#         if len(todos) == 0:
#             return Response("Todo does not exist", status=status.HTTP_404_NOT_FOUND)
#         serializer = TodosSerializer(todos, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = TodosSerializer(data=request.data)  # create new todo
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class TodoAPI(APIView):
#     def get(self, request, id=id):
#         todo = get_object_or_404(Todo, id=id)
#         if (todo.deleted_flag):  # check if the todo had been soft-deleted
#             return Response("Todo does not exist", status=status.HTTP_404_NOT_FOUND)
#         serializer = TodoSerializer(todo)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def patch(self, request, id):
#         todo = get_object_or_404(Todo, id=id)
#         if (request.data != {}):
#             todo.title = request.data['title']
#             todo.image = request.data['image']
#             todo.is_finished = request.data['is_finished']
#             todo.is_default = request.data['is_default']
#         else:
#             todo.deleted_flag = True  # soft-delete todo
#         todo.save()
#         serializer = TodosSerializer(todo)
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)