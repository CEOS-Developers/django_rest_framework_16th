# Create your views here.
import datetime

import django_filters
from django_filters import filters
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework import viewsets

from api.serializers import *


class TodoClassFilter(FilterSet):
    opened_todo_classes = filters.NumberFilter(field_name='is_open', lookup_expr='exact')
    searched_todo_class = filters.CharFilter(field_name='class_name', lookup_expr='contains')

    class Meta:
        model = TodoClass
        fields = ['is_open', 'class_name']


class TodoClassesViewSet(viewsets.ModelViewSet):
    queryset = TodoClass.objects.all()
    serializer_class = TodoClassSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoClassFilter


class TodoFilter(FilterSet):
    finished_todos = filters.BooleanFilter(field_name='is_finished', lookup_expr='exact')
    todo_title = filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = Todo
        fields = ['is_finished', 'title']


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter