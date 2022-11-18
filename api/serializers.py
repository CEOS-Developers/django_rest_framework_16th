from rest_framework import serializers
from .models import Goal, User


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'name', 'is_goal_private', 'color']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
