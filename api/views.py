"""
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
    def put(self, request, pk): => patch & delete partial=True
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
"""
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import *
from api.serializers import *
from .admin import UserCreationForm, UserChangeForm, UserAdmin
from django_filters.rest_framework import FilterSet, filters, DjangoFilterBackend


class TodoFilter(FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='iexact')
    contents = filters.CharFilter(field_name='contents', lookup_expr='contains')
    group = filters.NumberFilter(method='filter_group_notDone')

    class Meta:
        model = Todo
        fields = ['id', 'contents', 'group']

    def filter_group_notDone(self, queryset, group, value):
        queryset = Todo.objects.all()
        filtered_queryset = queryset.filter(group=value, status='not_done')
        return filtered_queryset


class JoinView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        form = UserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            user.nickname = form.clean_nickname()

            return Response({"message: Success Join"})

        else:
            return Response(form.errors)


class LoginView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        user = authenticate(email=request.data.get('email'), password=request.data.get('password'))
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return Response({"token": access_token})

        else:
            return Response("message: 존재하지 않는 사용자입니다")


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter
