from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Goal
from .serializers import GoalSerializer


# class GoalList(APIView):
#     def get(self, request, format=None):
#         goals = Goal.objects.all()
#         serializer = GoalSerializer(goals, many=True)
#         return Response({'data': serializer.data, 'message': "goal list get 요청 성공"}, status=HTTP_200_OK)
#
#     def post(self, request, format=None):
#         serializer = GoalSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'data': serializer.data, 'message': "goal post 요청 성공"}, status=HTTP_200_OK)
#         return Response({'data': serializer.errors, 'message': "goal post 실패"}, status=HTTP_400_BAD_REQUEST)
#
#
# class GoalDetail(APIView):
#     def get(self, request, pk):
#         goal = get_object_or_404(Goal, pk=pk)
#         serializer = GoalSerializer(goal)
#         return Response({'data': serializer.data, 'message': "goal detail get 요청 성공"}, status=HTTP_200_OK)
#
#     def delete(self, request, pk):
#         goal = get_object_or_404(Goal, pk=pk)
#         goal.delete()
#         return Response({'message': "goal delete 요청 성공"}, status=HTTP_200_OK)
#
#     def put(self, request, pk):
#         goal = get_object_or_404(Goal, pk=pk)
#         serializer = GoalSerializer(goal, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response({'data': serializer.data, 'message': "goal detail put 요청 성공"}, status=HTTP_200_OK)

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    
