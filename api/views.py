from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from . import serializers
from .common import *


class GoalView(APIView):
    def get(self, request):
        user = require_auth(request)
        if user is None:
            return JsonResponse(custom_response(401), status=401)

        goals = Goal.objects.filter(user_id=user.id)
        serializer = serializers.GoalSerializer(goals, many=True)
        return JsonResponse(custom_response(200, serializer.data), status=200)

    def post(self, request):
        user = require_auth(request)
        if user is None:
            return JsonResponse(custom_response(401), status=401)

        data = JSONParser().parse(request)
        new_data = {**data, "user": user.id}
        # ** : spread operator
        serializer = serializers.GoalSerializer(data=new_data)
        if not serializer.is_valid():
            return JsonResponse(custom_response(400, serializer.errors), status=400)
        serializer.save()
        return JsonResponse(custom_response(200, serializer.data), status=200)


class GoalDetailView(APIView):
    def get(self, request, pk):
        # 유저 검증
        goal = require_auth(request, self, pk)
        if goal is None:
            return JsonResponse(custom_response(401), status=401)

        serializer = serializers.GoalSerializer(goal)
        return JsonResponse(custom_response(200, serializer.data), status=200)

    def delete(self, request, pk):
        # 유저 검증
        goal = require_auth(request, self, pk)
        if goal is None:
            return JsonResponse(custom_response(401), status=401)

        goal.delete()
        return JsonResponse(custom_response(204), status=204)

    def put(self, request, pk):
        # 유저 검증
        goal = require_auth(request, self, pk)
        if goal is None:
            return JsonResponse(custom_response(401), status=401)

        data = JSONParser().parse(request)
        new_data = {**data, "user": goal.user.id}
        serializer = serializers.GoalSerializer(goal, data=new_data)
        if not serializer.is_valid():
            return JsonResponse(custom_response(400, serializer.errors), status=400)
        serializer.save()
        return JsonResponse(custom_response(200, serializer.data), status=200)
