from rest_framework import permissions
from api.models import *


class AuthCheck(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user_id = request.headers["userId"]
            # 값이 존재하지 않으면, try catch에 걸림
            Profile.objects.get(user_id=user_id)
            return True
        except:
            return False
