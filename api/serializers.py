from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        id = validated_data.get('id')
        nickname = validated_data.get('id')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            id=id,
            nickname=nickname,
            email=email,
            password=password
        )
        user.set_password(password)
        user.save()
        return user


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