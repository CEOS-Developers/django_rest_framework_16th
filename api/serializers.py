from rest_framework import serializers
from api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile# 사용할 모델
        fields = ['user','image','nickname','message']  # 사용할 모델의 필드

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList# 사용할 모델
        fields = ['profile','description','date_created']  # 사용할 모델의 필드
