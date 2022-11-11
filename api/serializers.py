from rest_framework import serializers

from api.models import Todo, TodoClass


class TodoClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoClass
        fields = [
            'id',
            'user',
            'class_name',
            'class_color',
            'is_open',
            'created_at',
            'updated_at',
            'deleted_flag'
        ]


class TodoClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoClass
        fields = [
            'id',
            'user',
            'class_name',
            'class_color',
            'is_open',
            'created_at',
            'updated_at',
            'deleted_flag'
        ]


class TodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            'id',
            'todo_class',
            'title',
            'image',
            'is_finished',
            'is_default',
            'created_at',
            'updated_at',
            'deleted_flag'
        ]


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            'id',
            'todo_class',
            'title',
            'image',
            'is_finished',
            'is_default',
            'created_at',
            'updated_at',
            'deleted_flag',
        ]
