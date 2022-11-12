# response 커스텀
def custom_response(status_code, data=[]):
    if status_code < 300:
        message = "SUCCESS"
    elif status_code < 400:
        message = ""
    else:
        if status_code == 400:
            message = "잘못된 요청입니다."
        elif status_code == 401:
            message = "인증된 유저가 아닙니다."
        elif status_code == 403:
            message = "해당 권한이 없습니다."
        elif status_code == 404:
            message = "데이터를 찾을 수 없습니다."
    return {"status": status_code, "message": message, 'data': data}


