from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from api.models import Todo, TodoClass, User


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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('nickname', 'username', 'password', 'password2', 'email')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            nickname=validated_data['nickname']
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"message" : "존재하지 않는 사용자입니다"}
        )
