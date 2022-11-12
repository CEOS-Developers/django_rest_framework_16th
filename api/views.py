import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import *
from api.serializers import *
from rest_framework.views import APIView
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, timedelta

# Create your views here.

class TodoFilter(FilterSet):
    user = filters.ModelChoiceFilter(queryset=User.objects.all())
    disclosure_choice = filters.TypedChoiceFilter(choices=Todo.DISCLOSURE_CHOICES)
    recent_todos = filters.BooleanFilter(method='filter_recent_todos', label='recent_todos')
    class Meta:
        model = Todo
        fields = ['user', 'disclosure_choice']

    def filter_recent_todos(self, queryset, name, value):
        queryset = Todo.objects.all()
        filtered_queryset = queryset.filter(date__gte=datetime.now()-timedelta(days=7))
        filtered_queryset_false = queryset.exclude(pk__in=filtered_queryset)

        if(value==True):
            return filtered_queryset
        else:
            return filtered_queryset_false


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter


"""
#Class-Based View
class TodoList(APIView):
    def get(self, request, format=None):
        todo_items = Todo.objects.all()
        serializer = TodoSerializer(todo_items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class TodoItem(APIView):
    def get(self, request, pk, format=None):
        todo = Todo.objects.filter(id=pk)
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        todo_instance = Todo.objects.get(id=pk)
        serializer = TodoSerializer(instance=todo_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    def delete(self, request, pk, format=None):
        todo = Todo.objects.filter(id=pk)
        todo.delete()
        return Response(status=201)
        
        
#Function-Based View
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
@api_view(['GET', 'PUT', 'DELETE'])
def todo_item(request, pk):

    if request.method == 'GET':
        todo = Todo.objects.filter(id=pk)
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        todo_instance = Todo.objects.get(id=pk)
        serializer = TodoSerializer(instance=todo_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        todo = Todo.objects.filter(id=pk)
        todo.delete()
        return Response(status=201)


"""