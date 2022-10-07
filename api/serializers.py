from rest_framework import serializers
from api.models import *


class TodoSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    goal_name = serializers.SerializerMethodField()
    todo_like = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ['user', 'goal', 'content', 'date', 'state', 'like_count',
                  'user_name', 'goal_name', 'todo_like']

    def get_user_name(self, obj):
        return obj.user.username

    def get_goal_name(self, obj):
        return obj.goal.name

    def get_todo_like(self, obj):
        return list(Like.objects.filter(todo_id=obj.id).prefetch_related('like_todo').values())


class GoalSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    goal_todos = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = ['user', 'name', 'privacy', 'username', 'goal_todos']

    def get_user_name(self, obj):
        return obj.user.username

    def get_goal_todos(self, obj):
        return list(Todo.objects.filter(goal_id=obj.id).prefetch_related('todo_goal').values())


class UserSerializer(serializers.ModelSerializer):
    user_goals = serializers.SerializerMethodField()
    user_todos = serializers.SerializerMethodField()
    user_follower = serializers.SerializerMethodField()
    user_following = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = {'nickname', 'email', 'password', 'is_active', 'user_goals', 'user_todos',
                  'user_follower', 'user_following', 'created_at'}

    def get_user_goals(self, obj):
        return list(Goal.objects.filter(user_id=obj.id).prefetch_related('goal_user').values())

    def get_user_todos(self, obj):
        return list(Todo.objects.filter(user_id=obj.id).prefetch_related('todo_user').values())

    def get_user_follower(self, obj):
        return list(Follow.objects.filter(follower_id=obj.id).prefetch_related('follower').values())

    def get_user_following(self, obj):
        return list(Follow.objects.filter(following_id=obj.id).prefetch_related('following').values())

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")


class LikeSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Like
        fields = ['user', 'todo', 'username']

    def get_user_name(self, obj):
        return obj.user.username


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following']
