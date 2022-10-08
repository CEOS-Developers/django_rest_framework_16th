from rest_framework import serializers
from api.models import Goal, Todo

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['user_name', 'goal_name', 'is_public', 'color', 'created_at', 'updated_at', 'deleted_at']

class TodoSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)
    todo_content = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ['user_name', 'goal_name', 'content', 'is_done', 'is_stored', 'done_date', 'created_at', 'updated_at', 'deleted_at']

    def get_todo_content(self, obj):
        return obj.todo_content