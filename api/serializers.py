from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('follower', 'following')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_name', 'user')

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('todo_name', 'user', 'category', 'disclosure_choice', 'date')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('todo', 'author', 'emoji', 'comment')