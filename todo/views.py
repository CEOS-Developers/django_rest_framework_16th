from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Goal, Todo
from .serializers import GoalSerializer


@csrf_exempt
def goal_list(request):
    if request.method == 'GET':
        goals = Goal.objects.all()
        serializer = GoalSerializer(goals, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = GoalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def goal_detail(request, pk):
    if request.method == 'GET':
        goal = Goal.objects.get(pk=pk)
        serializer = GoalSerializer(goal)
        return JsonResponse(serializer.data, safe=False)
