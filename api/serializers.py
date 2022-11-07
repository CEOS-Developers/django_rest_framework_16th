from rest_framework import serializers
from .models import Goal, User, Profile


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'name', 'is_goal_private', 'color']
