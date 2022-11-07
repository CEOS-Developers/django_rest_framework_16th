from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Profile
        fields = ['user', 'introduction', 'search_yn', 'open_yn',
                  'start_sunday_yn', 'order_desc_yn', 'input_top_yn', 'check_likes_yn']


class TodoGroupSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = TodoGroup
        fields = ['user', 'group', 'opened', 'color']


class TodoListSerializer(serializers.ModelSerializer):
    user = UserSerializer
    group = TodoGroupSerializer

    class Meta:
        model = TodoList
        fields = ['user', 'group', 'start_date', 'end_date', 'repeated_day', 'alarm_time', 'todo', 'status']
