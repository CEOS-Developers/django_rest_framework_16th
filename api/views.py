from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from api.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.delete()
        user.save()
        return Response(data='delete user success')


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def destroy(self, request, *args, **kwargs):
        goal = self.get_object()
        goal.delete()
        goal.save()
        return Response(data='delete success')


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def destroy(self, request, *args, **kwargs):
        todo = self.get_object()
        todo.delete()
        todo.save()
        return Response(data='delete success')


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def destroy(self, request, *args, **kwargs):
        like = self.get_object()
        like.delete()
        like.save()
        return Response(data='delete success')

class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def destroy(self, request, *args, **kwargs):
        follow = self.get_object()
        follow.delete()
        follow.save()
        return Response(data='delete success')
