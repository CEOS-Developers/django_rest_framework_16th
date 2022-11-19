from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    login_id = serializers.CharField(
        required=True,
        write_only=True,
        max_length=30
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    email = serializers.CharField(
        required=True,
        write_only=True,
        max_length=255
    )

    class Meta:
        model = User
        fields = '__all__'

    def save(self, validated_data):
        login_id = validated_data.get('login_id')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            login_id=login_id,
            email=email
        )
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        login_id = data.get('login_id', None)

        # 이미 존재하는 계정인지 확인
        if User.objects.filter(login_id=login_id).exists():
            raise serializers.ValidationError("User already exists")
        return data


class LoginSerializer(serializers.ModelSerializer):
    login_id = serializers.CharField(
        required=True,
        write_only=True,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type' : 'password'}
    )

    class Meta:
        model = User
        fields = ['login_id', 'password']

    def validate(self, data):
        login_id = data.get('login_id', None)
        password = data.get('password', None)

        if User.objects.filter(login_id=login_id).exists():
            user = User.objects.get(login_id=login_id)

            if not user.check_password(password):
                raise serializers.ValidationError("wrong password")
        else:
            raise serializers.ValidationError("user account not exist")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            'user': user,
            'refresh_token': refresh_token,
            'access_token': access_token,
        }

        return data



