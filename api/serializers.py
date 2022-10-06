from rest_framework import serializers
from .models import Todo, User


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user_id'])
        if user:
            todo = Todo.objects.create(
                user=user,
                contents=validated_data['contents'],
                date=validated_data['date'],
            )
            todo.save()
            return "할 일 생성에 성공하였습니다."
        else:
            return "해당 유저를 확인할 수 없습니다."

    def delete(self, pk):
        todo = Todo.objects.filter(id=pk)
        if todo:
            todo.delete()
            return "삭제 완료"
        else:
            return "해당 할 일이 존재하지 않습니다."

    def update(self, pk, validated_data):
        todo = Todo.objects.filter(id=pk)
        if todo:
            todo.contents = validated_data.get('contents', todo.contents)
            todo.date = validated_data.get('date', todo.date)
            todo.is_checked = validated_data.get('is_checked', todo.is_checked)
            todo.save()
            return "업데이트 완료"
        else:
            return "해당 할 일이 존재하지 않습니다."


class UserSerializer(serializers.ModelSerializer):

    todo_list = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'web_id', 'web_pw', 'intro_text', 'todo_list', 'created_at', 'updated_at']