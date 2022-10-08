from rest_framework.views import APIView
from api.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser

from . import serializers


# response 커스텀
def customResponse(status_code, data=""):
    if status_code < 300:
        message = "SUCCESS"
        if not data:
            return {"status": status_code, "message": message}
        return {"status": status_code, "message": message, 'data': data}
    elif status_code < 400:
        message = ""
    else:
        message = "FAIL"

    if not data:
        return {"status": status_code, "message": message}
    return {"status": status_code, "message": message, 'error': data}


class GoalView(APIView):
    def get(self, request):
        user_id = request.headers["userId"]
        user = Profile.objects.get(user_id=user_id)
        if not user:
            return JsonResponse(customResponse(400), status=400)

        goals = Goal.objects.filter(user_id=user.id)
        serializer = serializers.GoalSerializer(goals, many=True)
        return JsonResponse(customResponse(200, serializer.data), status=200)

    def post(self, request):
        user_id = request.headers["userId"]
        user = Profile.objects.get(user_id=user_id)
        if not user:
            return JsonResponse(customResponse(400), status=400)

        data = JSONParser().parse(request)
        new_data = {**data, "user": user.id}
        serializer = serializers.GoalSerializer(data=new_data)
        if not serializer.is_valid():
            return JsonResponse(customResponse(400, serializer.errors), status=400)
        serializer.save()
        return JsonResponse(customResponse(201, serializer.data), status=201)


class GoalDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Goal, pk=pk)

    def get(self, request, pk):
        # 유저 검증
        goal = self.get_object(pk)
        user_id = request.headers["userId"]
        if not int(user_id) == goal.user.user_id:
            return JsonResponse(customResponse(400), status=400)

        serializer = serializers.GoalSerializer(goal)
        return JsonResponse(customResponse(200, serializer.data), status=200)

    def delete(self, request, pk):
        # 유저 검증
        goal = self.get_object(pk)
        user_id = request.headers["userId"]
        if not int(user_id) == goal.user.user_id:
            return JsonResponse(customResponse(400), status=400)

        goal.delete()
        return JsonResponse(customResponse(204), status=204)

    def put(self, request, pk):
        # 유저 검증
        user_id = request.headers["userId"]
        goal = self.get_object(pk)
        if not int(user_id) == goal.user.user_id:
            return JsonResponse(customResponse(400), status=400)

        data = JSONParser().parse(request)
        serializer = serializers.GoalSerializer(goal, data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400, safe=False)
        serializer.save()

        return JsonResponse(serializer.data, status=201, safe=False)
