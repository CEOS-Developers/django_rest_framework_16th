# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포

## 2주차 : 2주차 미션: DB 모델링 및 Django ORM
## Todomate
### Todomate란?
일정 관리 + 타인과 일정 공유
### 기능
1. 해야 할 일을 목표별로 나눠 저장
2. 일기 작성 가능
3. 팔로워와 자신의 일정을 공유하고, 일기와 할 일에 관해 좋아요(이모지)를 남길 수 있음

## ERD
![erd](https://user-images.githubusercontent.com/67852689/194323547-a46512ce-d500-45fd-9a0e-f727be3859e8.jpeg)
* Profile : Django의 유저모델과 OneToOne 확장 이용, 유저의 정보를 저장
* Goal : 목표에 대한 정보를 저장
  * 1(User) : N(Goal) : 유저가 여러 개의 목표를 생성할 수 있다.
  * 1(Goal) : N(Todo) : 한 목표에 여러 투두를 생성할 수 있다.
* Todo : 투두에 관한 정보를 저장
  * 1(Goal) : N(Todo)
* TodoLike : 투두의 좋아요 정보를 저장
  * 1(Todo) : N(TodoLike) : 한 투두에 많은 수의 좋아요를 가질 수 있다.
  * 1(User) : 1(TodoLike) : 한 명의 유저가 좋아요 하나만 남길 수 있으므로 1 대 1이다.
* Diary : 일기에 관한 정보를 저장
  * 1(User) : N(Diary) : 일기를 날짜별로 적을 수 있다. 그러므로 유저 한 명은 여러 개의 일기를 적을 수 있다.
* DiaryLike : 일기의 좋아요 정보를 저장
  * 1(Diary) : N(DiaryLike) : 일기도 투두와 마찬가지로 많은 수의 좋아요를 가질 수 있다.
  * 1(User) : 1(DiaryLike) : Todo 좋아요와 이유는 동일하다
* Follow : 팔로우 관련 정보를 저장
  * 1(User) : N(Following) : 한 유저와 많은 수의 유저가 팔로우 관계를 맺을 수 있다.

## migration
```shell
python manage.py makemigrations api
python manage.py migrate api
```
* makemigrations : 모델을 변경시킨 사실 또는 새로 생성한 모델들과 같은 변경사항을 migrations로 저장
* migration : Django가 모델의 변경사항을 저장

## ORM 사용해보기
![image](https://user-images.githubusercontent.com/67852689/193402878-b9dd40d1-ad7b-4a91-9161-ef7e1d41a918.png)
> 유저 모델 객체 3개

![image](https://user-images.githubusercontent.com/67852689/193402877-da27e1b4-ca98-4622-8f2f-517e256dd3fd.png)
> 유저 테이블 인스턴스를 외래키로 가지는 인스턴스를 생성 및 조회

![image](https://user-images.githubusercontent.com/67852689/193402880-cea2dcf2-65ae-4b6b-8ac3-997a42fd9007.png)
> filter를 이용해 조회

## 회고
1. django.db.utils.IntegrityError: (1048, "Column 'user_id' cannot be null")<br>
Profile 인스턴스를 만들면 User가 자동으로 생성되는 줄 알았으나, 아니었다. 장고는 User를 자동적으로 생성해 주지 않기 때문에, Profile 인스턴스를 만들기 위해선,
먼저 User 인스턴스를 만들어줘야 한다.
2. MySQLdb.ProgrammingError: (1146, "Table 'todo.api_profile' doesn't exist")<br>
결론부터 말하자면, 디비 문제였다. User 테이블의 이름을 Profile로 바꾸면서 디비에 저장되어 있던 데이터와 코드에 적혀있는 모델과의 차이 때문에 발생했던 것 같다.
디비를 초기화하고 migration 파일을 모두 삭제해서, 문제를 해결할 수 있었다.
3. 어렵다<br>
그래도 프론트보단 좋다ㅋ

---

## 3주차 : DRF1 : Serializer
## 데이터 삽입
![image](https://user-images.githubusercontent.com/67852689/194706621-b1a21901-663b-4eb2-942e-9feff43498a8.png)
> Profile
![image](https://user-images.githubusercontent.com/67852689/194706738-8fac3407-6408-41bd-a4d4-f6dac33a2de7.png)
> Goal

## API
### 모든 데이터를 가져오는 API 만들기
* url : http://127.0.0.1:8000/api/goal
* method : get
```json
{
    "status": 200,
    "message": "SUCCESS",
    "data": [
        {
            "id": 6,
            "user": 5,
            "name": "ggsadasddasd",
            "is_goal_private": false,
            "color": ""
        },
        {
            "id": 7,
            "user": 5,
            "name": "g4",
            "is_goal_private": false,
            "color": ""
        },
        {
            "id": 8,
            "user": 5,
            "name": "g5",
            "is_goal_private": false,
            "color": ""
        }
    ]
}
```
### 특정 데이터를 가져오는 API 만들기
* url : http://127.0.0.1:8000/api/goal/7
* method : get
```json
{
    "status": 200,
    "message": "SUCCESS",
    "data": {
        "id": 7,
        "user": 5,
        "name": "g4",
        "is_goal_private": false,
        "color": ""
    }
}
```
### 새로운 데이터를 create하도록 요청하는 API 만들기
* url : http://127.0.0.1:8000/api/goal
* method : post
```json
{
    "status": 200,
    "message": "SUCCESS",
    "data": {
        "id": 8,
        "user": 5,
        "name": "g5",
        "is_goal_private": false,
        "color": ""
    }
}
```
### 특정 데이터를 삭제 또는 업데이트하는 API
#### 삭제
* url : http://127.0.0.1:8000/api/goal/5
* method : delete
```json
{
    "status": 204,
    "message": "SUCCESS"
}
```
#### 업데이트
* url : http://127.0.0.1:8000/api/goal/5
* method : delete
```json
{
    "status": 200,
    "message": "SUCCESS",
    "data": {
        "id": 6,
        "user": 5,
        "name": "ggsadasddasd",
        "is_goal_private": false,
        "color": ""
    }
}
```
## 회고
* 코드상 중복되는 부분이 많다. 다음엔 중복을 제거해 봐야겠다
* 토큰을 사용하지 않아서 요청 헤더에 유저 정보를 넣어보냈다. 토큰을 여기에 적용시킨다면, 토큰을 이용해 유저 인증을 한 후, api가 작동하도록 만들 것이다.
* 잘 작동하긴 하는데, 잘 만든지 모르겠다.

---

## 4주차 : DRF2 - API View & Viewset & Filter
## DRF API View 의 CBV 으로 리팩토링
```python
class GoalView(APIView):
    def get(self, request):
        user = require_auth(request)
        if user is None:
            return JsonResponse(custom_response(401), status=401)

        goals = Goal.objects.filter(user_id=user.id)
        serializer = serializers.GoalSerializer(goals, many=True)
        return JsonResponse(custom_response(200, serializer.data), status=200)
```
이미 DRF API View의 CBV 방식으로 만들었기 때문에, FBV를 CBV로 변경할 필요 없었다. 지난번 리뷰 때 지적받았던 부분을 수정 후 주석 처리했다.
### 수정 부분
* url 수정
* 유저 인증 부분을 require_auth로 통합
* custom_response, require_auth 함수를 common.py로 이동

## Viewset으로 리팩토링하기
```python

```
이전 코드에서도 구현했던, 유저 검증과 response custom을 똑같이 구현했다
* 유저 검증
```python
# permission.py

class AuthCheck(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user_id = request.headers["userId"]
            # 값이 존재하지 않으면, try catch에 걸림
            Profile.objects.get(user_id=user_id)
            return True
        except:
            return False
```
* response custom
```python
# util.py

class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = renderer_context.get('response')

        response = custom_response(response_data.status_code, data)

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)
```
```python
# base.py (setting.py)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'api.util.CustomRenderer',
    ]
}
```
setting.py에 default renderer를 추가하여, 커스텀 리스폰스를 구현함
## filter 기능 구현하기
## 공부한 내용 정리 및 회고