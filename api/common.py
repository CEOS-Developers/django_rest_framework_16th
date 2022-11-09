from api.models import *


# response 커스텀
def custom_response(status_code, data=""):
    if status_code < 300:
        message = "SUCCESS"
        if not data:
            return {"status": status_code, "message": message}
        return {"status": status_code, "message": message, 'data': data}
    elif status_code < 400:
        message = ""
    else:
        message = "FAIL"

    if not data:
        return {"status": status_code, "message": message}
    return {"status": status_code, "message": message, 'error': data}


def require_auth(request, self=0, pk=0):
    try:
        # 유저의 존재 유무 검사
        user_id = request.headers["userId"]
        user = Profile.objects.get(user_id=user_id)
        if self == 0:
            return user
        else:
            # 유저가 존재하고 해당 목표에 접근할 수 있는지 판단
            goal = Goal.objects.get(pk=pk)
            user_id = request.headers["userId"]
            if not int(user_id) == goal.user.user_id:
                raise
                # throw err
            return goal
    except:
        return None
