from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from api.serializers import *


@csrf_exempt
def todo_lists(request):
    if request.method == 'GET':
        lists = TodoList.objects.all()
        serializer = TodoListSerializer(lists, many=True)
        return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TodoListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def todo_list(request, pk):
    if request.method == 'GET':
        todolist = TodoList.objects.get(id=pk)
        serializer = TodoListSerializer(todolist)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        todolist = TodoList.objects.get(id=pk)
        todolist.delete()

        return JsonResponse(status=200)
