from django.http import JsonResponse
from rest_framework.status import *
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Goal, Todo
from .serializers import GoalSerializer


class GoalList(APIView):
    def get(self, request, format=None):
        goals = Goal.objects.all()
        serializer = GoalSerializer(goals, many=True)
        return Response({'data': serializer.data, 'message': "goal list get 요청 성공"}, status=HTTP_200_OK)

    def post(self, request, format=None):
        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': "goal post 요청 성공"}, status=HTTP_200_OK)
        return Response({'data': serializer.errors, 'message': "goal post 실패"}, status=HTTP_400_BAD_REQUEST)


def goal_detail(request, pk):
    if request.method == 'GET':
        goal = Goal.objects.get(pk=pk)
        serializer = GoalSerializer(goal)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'DELETE':
        goal = Goal.objects.get(pk=pk)
        goal.delete()
        return JsonResponse({'data': '삭제 성공'})

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        goal = Goal.objects.get(pk=pk)
        serializer = GoalSerializer(goal, data=data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data, safe=False)
