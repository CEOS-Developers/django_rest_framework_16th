from .models import Goal, Todo
from rest_framework import serializers


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['user', 'title', 'privacy', 'color']
