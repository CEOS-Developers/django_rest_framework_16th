# import datetime
#
# from django.shortcuts import get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
#
# @csrf_exempt
# @api_view(['GET','POST'])
# def TodoAPI(request):
#     if request.method == 'GET':
#         todos = Todo.objects.filter(deleted_at=None) # filter out soft-deleted todos
#         if len(todos) == 0:
#             return Response("Todo does not exist", status=status.HTTP_404_NOT_FOUND)
#         serializer = TodosSerializer(todos, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = TodosSerializer(data=request.data) # create new todo
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)