from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from api.models import *


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = ['created_at', 'updated_at', 'deleted_at', 'is_deleted']


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'nickname', 'password', 'introduce', 'image', 'is_public', 'search', 'is_active', 'is_superuser']


class JoinSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'nickname', 'password', 'password2')

    def validate(self, request):
        if request['password'] != request['password2']:
            raise serializers.ValidationError({"Password doesn't match."})
        return request

    def save(self, request):
        user = User.objects.create_user(
            email=self.validated_data['email'],
            nickname=self.validated_data['nickname'],
            password=self.validated_data['password']
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, request):
        email = request.get('email', None)
        password = request.get('password', None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError({"Wrong Password"})
        else:
            raise serializers.ValidationError({"User doesn't exist."})

        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            'email': user.email,
            'refresh': refresh,
            'access': access
        }

        return data


class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Follow
        fields = ['follower', 'following']


class TodoSerializer(BaseModelSerializer):
    user = UserSerializer
    # category_title = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ['todo_id', 'user', 'category', 'is_success', 'is_valid', 'deadline', 'alarm', 'content']

    # def get_category_title(self, obj):
    #     return obj.category.title


class CategorySerializer(BaseModelSerializer):
    user = UserSerializer
    todos = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_id', 'user', 'title', 'color', 'is_public']
