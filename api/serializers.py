from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import *


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = ['created_at', 'updated_at', 'deleted_at', 'is_deleted']


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'nickname', 'password', 'introduce', 'image', 'is_public', 'search']


class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Follow
        fields = ['follower', 'following']


class TodoSerializer(BaseModelSerializer):
    user = UserSerializer
    # category_name = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ['todo_id', 'user', 'category', 'is_success', 'is_valid', 'deadline', 'alarm', 'content']

    # def get_category_title(self, obj):  # 질문: static으로 선언해야 하나요?
    #     return obj.category.title


class CategorySerializer(BaseModelSerializer):
    user = UserSerializer
    todos = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_id', 'user', 'title', 'color', 'is_public']
