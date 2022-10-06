from rest_framework import serializers

from api.models import Todo, TodoClass


class TodoClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoClass
        fields = [
            'user',
            'class_name',
            'class_color',
            'is_open',
            'created_at',
            'updated_at',
            'deleted_at'
        ]

class TodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            'todo_class',
            'title',
            'image',
            'is_finished',
            'is_default',
            'created_at',
            'updated_at',
            'deleted_at'
        ]