from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import viewsets

from api.serializers import *
from api.filters import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['username', 'email', 'is_staff', 'is_active']
    ordering_fields = ['username', 'last_login']
    ordering = ['username']

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.delete()
        user.save()
        return Response(data='delete user success')


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['name', 'user', 'privacy']
    ordering_fields = ['name']
    ordering = ['name']


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # filter_class = TodoFilter
    filterset_fields = ['state', 'content', 'user', 'goal']
    ordering_fields = ['date', 'like_count']
    ordering = ['date']


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
