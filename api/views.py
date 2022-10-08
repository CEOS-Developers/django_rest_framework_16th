# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.models import ToDo
from api.serializers import ToDoSerializer


@csrf_exempt
def todo_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':  # 모든 데이터 얻기
        todo = ToDo.objects.all()
        serializer = ToDoSerializer(todo, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':  # 새로운 데이터 등록
        data = JSONParser().parse(request)
        serializer = ToDoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def todo_one(request, id):
    if request.method == 'GET':  # 특정 데이터 얻기
        todo = ToDo.objects.get(id=id)
        serializer = ToDoSerializer(todo, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'DELETE':  # 특정 데이터 삭제
        todo = ToDo.objects.get(id=id)
        todo.delete()
        return JsonResponse(status=202)

    elif request.method == 'PUT':  # 특정 데이터 업데이트
        data = JSONParser().parse(request)
        todo = ToDo.objects.get(id=id)
        todo.update(**data)
        return JsonResponse(status=200)
