from rest_framework import serializers
from api.models import ToDo


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo  # 사용할 모델
        fields = '__all__'  # 사용할 모델 필드
