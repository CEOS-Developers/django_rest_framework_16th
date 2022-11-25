# views.py
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, status
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from .serializers import *
from .models import Todo, User

class TodoListFilter(FilterSet):
    contents = filters.CharFilter(field_name='contents', lookup_expr='icontains')
    is_done = filters.BooleanFilter(method='filter_is_done')

    class Meta:
        model = Todo
        fields = ['contents', 'is_checked']

    def filter_is_done(self, queryset, name, value):
        return queryset.filter(type=value)


class TodoListViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoListFilter


class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))

        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "message": "login success",
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
        else:
            return Response({"message": "login fail"}, status=status.HTTP_400_BAD_REQUEST)



# # CBV
# class TodoListsAPI(APIView):
#     def get(self, request):
#         items = TodoSerializer(Todo.objects.all(), many=True)
#         return Response(items.data)
#
#     def post(self, request):
#         req_data = JSONParser().parse(request)
#         result = TodoSerializer.create(TodoSerializer, req_data)
#         return Response(result)
#
#
# # 특정 데이터(TodoList)를 가져오는 API
# class TodoListAPI(APIView):
#     def get(self, request, pk):
#         item = TodoSerializer(Todo.objects.get(id=pk))
#         return Response(item.data)
#
#     def delete(self, request, pk):
#         result = TodoSerializer.delete(TodoSerializer, pk)
#         return Response(result)
#
#     def put(self, request, pk):
#         req_data = JSONParser().parse(request)
#         result = TodoSerializer.update(TodoSerializer, pk, req_data)
#         return Response(result)
