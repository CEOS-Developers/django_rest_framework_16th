from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate

from api.models import *
from api.forms import *
from api.serializers import *

# from rest_framework.parsers import JSONParser

# from django.http import JsonResponse
# from django.shortcuts import  get_object_or_404


class TodoFilter(FilterSet):
    user = filters.CharFilter(method='user_filter')
    is_deleted = filters.BooleanFilter(method='delete_filter')
    content = filters.CharFilter(field_name='content', lookup_expr='icontains')

    class Meta:
        model = Todo
        fields = ['user', 'content']

    def user_filter(self, queryset, user, value):
        filtered_queryset = queryset.filter(**{
            user: value,
        })

        return filtered_queryset

    def delete_filter(self, queryset, boolean):
        queryset = Todo.objects.all()
        filtered_queryset = queryset.filter(deleted_at__isnull=boolean)

        return filtered_queryset


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter


class JoinView(APIView):
    serializer_class = JoinSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "email": user.email,
                    "nickname": user.nickname,
                    "message": "가입이 성공적으로 이뤄졌습니다.",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            email = serializer.validated_data['email']
            access = serializer.validated_data['access']
            refresh = serializer.validated_data['refresh']
            # data = serializer.validated_data
            res = Response(
                {
                    "message": "로그인되었습니다.",
                    "email": email,
                    "access": access,
                    "refresh": refresh
                },
                status=status.HTTP_200_OK,
            )
            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Test(APIView):
    def get(self, request):
        res = Response(
            {
                "hello world"
            },
            status=status.HTTP_200_OK,
        )
        return res


# class TodoList(APIView):
#     def get(self, request):
#         todos = Todo.objects.filter(deleted_at=None)
#         serializer = TodoSerializer(todos, many=True)
#         return JsonResponse(serializer.data, safe=False, status=200)
#
#     def post(self, request):
#         data = JSONParser().parse(request)
#         serializer = TodoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# class TodoDetail(APIView):
#     def get(self, request, pk):
#         todo = Todo.objects.filter(todo_id=pk)
#         serializer = TodoSerializer(todo, many=True)
#         return JsonResponse(serializer.data, safe=False, status=200)
#
#     def delete(self, request, pk):
#         todo = get_object_or_404(Todo, todo_id=pk)
#         todo.delete()
#         return Response(status=200)
#
#     def patch(self, request, pk):
#         todo = get_object_or_404(Todo, todo_id=pk)
#         data = JSONParser().parse(request)
#         serializer = TodoSerializer(instance=todo, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=200)
#         return JsonResponse(serializer.errors, status=400)
