from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['user_id', 'nickname']


# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer
#
#     class Meta:
#         model = Profile
#         fields = ['user', 'introduction', 'search_yn', 'open_yn',
#                   'start_sunday_yn', 'order_desc_yn', 'input_top_yn', 'check_likes_yn']
#

class TodoGroupSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = TodoGroup
        fields = ['user', 'group', 'opened', 'color']


class TodoSerializer(serializers.ModelSerializer):
    user = UserSerializer
    group = TodoGroupSerializer

    class Meta:
        model = Todo
        fields = ['user', 'group', 'contents', 'status']
