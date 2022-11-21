from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile# 사용할 모델
        fields = ['user','image','nickname','message']  # 사용할 모델의 필드

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList# 사용할 모델
        fields = ['profile','description','date_created']  # 사용할 모델의 필드
#
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
#
#     def create(self, validated_data):
#         login_id = validated_data.get('login_id')
#         password = validated_data.get('password')
#         user = User(
#             login_id=login_id,
#         )
#         user.set_password(password)
#         user.save()
#         return user
