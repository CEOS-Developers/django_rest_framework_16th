from rest_framework import serializers
from api.models import *

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['user_name', 'class_name', 'is_public', 'color']

class TodoSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)
    todo_content = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ['user_name', 'goal_name', 'content', 'is_done', 'is_stored', 'done_date']

    def get_todo_content(self, obj):
        return obj.todo_content