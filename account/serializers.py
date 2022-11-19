from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *


class UserLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        user_id = data.get("user_id", None)
        password = data.get("password", None)

        if User.objects.filter(user_id=user_id).exists():
            user = User.objects.get(user_id=user_id)
            if not user.check_password(password):
                raise serializers.ValidationError('일치하지 않는 비밀번호입니다')
            else:
                token = RefreshToken.for_user(user)
                refresh = str(token)
                access = str(token.access_token)

                data = {
                    'user': user.user_id,
                    'access_token': access,
                }

                return data
        else:
            raise serializers.ValidationError('존재하지 않는 사용자입니다')