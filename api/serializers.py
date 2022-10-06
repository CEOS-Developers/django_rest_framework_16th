from rest_framework import serializers
from api.models import TodoList


class TodoListSerializer(serializers.Serializer):
    class Meta:
        model = TodoList
        fields = ['user', 'group', 'start_date', 'end_date', 'repeated_day', 'alarm_time', 'todo', 'image', 'status']

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return TodoList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.user = validated_data.get('user', instance.user)
        instance.group = validated_data.get('group', instance.group)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.repeated_day = validated_data.get('repeated_day', instance.repeated_day)
        instance.alarm_time = validated_data.get('alarm_time', instance.alarm_time)
        instance.todo = validated_data.get('todo', instance.todo)
        instance.image = validated_data.get('image', instance.image)
        instance.status = validated_data.get('status', instance.status)

        instance.save()
        return instance
