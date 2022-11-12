# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import viewsets

from .serializers import *

class TodoListViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

# # CBV
# class TodoListsAPI(APIView):
#     def get(self, request):
#         items = TodoSerializer(Todo.objects.all(), many=True)
#         return Response(items.data)
#
#     def post(self, request):
#         req_data = JSONParser().parse(request)
#         result = TodoSerializer.create(TodoSerializer, req_data)
#         return Response(result)
#
#
# # 특정 데이터(TodoList)를 가져오는 API
# class TodoListAPI(APIView):
#     def get(self, request, pk):
#         item = TodoSerializer(Todo.objects.get(id=pk))
#         return Response(item.data)
#
#     def delete(self, request, pk):
#         result = TodoSerializer.delete(TodoSerializer, pk)
#         return Response(result)
#
#     def put(self, request, pk):
#         req_data = JSONParser().parse(request)
#         result = TodoSerializer.update(TodoSerializer, pk, req_data)
#         return Response(result)
