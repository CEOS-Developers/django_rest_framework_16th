from rest_framework import serializers

from .models import *


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['id', 'user', 'contents', 'date', 'is_checked', 'created_at', 'updated_at']


    # def create(self, validated_data):
    #     try:
    #         user = User.objects.get(id=validated_data['user_id'])
    #     except User.DoesNotExist:
    #         return {"message": "해당 유저를 찾을 수 없습니다."}
    #     else:
    #         todo = Todo.objects.create(
    #             user=user,
    #             contents=validated_data['contents'],
    #             date=validated_data['date'],
    #         )
    #         todo.save()
    #         ret_object = {
    #             "message": "할 일을 생성하였습니다.",
    #             "data": TodoSerializer(todo).data
    #         }
    #         return ret_object
    #
    # def delete(self, pk):
    #     try:
    #         todo = Todo.objects.get(id=pk)
    #     except Todo.DoesNotExist:
    #         return {"message": "해당 기록을 찾을 수 없습니다."}
    #     else:
    #         ret_object = {"message": "삭제 성공"}
    #         todo.delete()
    #         return ret_object
    #
    #
    # def update(self, pk, validated_data):
    #     try:
    #         todo = Todo.objects.get(id=pk)
    #     except Todo.DoesNotExist:
    #         return {"message": "해당 기록을 찾을 수 없습니다."}
    #     else:
    #         todo.contents = validated_data.get('contents', todo.contents)
    #         todo.date = validated_data.get('date', todo.date)
    #         todo.is_checked = validated_data.get('is_checked', todo.is_checked)
    #         todo.save()
    #         ret_object = {
    #             "message": "업데이트 완료",
    #             "data": TodoSerializer(todo).data
    #         }
    #         return ret_object

class UserSerializer(serializers.ModelSerializer):

    todo_list = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'web_id', 'web_pw', 'intro_text', 'todo_list', 'created_at', 'updated_at']