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
* viewset으로 리팩토링
```python
# view.py

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GoalSerializer
    queryset = Goal.objects.all()
    permission_classes = [AuthCheck]
    filter_backends = [DjangoFilterBackend]
    # filter_class = GoalFilter
    filterset_fields = ['is_goal_private', 'name', 'id']
```
* router 사용
```python
# url.py

router = routers.DefaultRouter()
router.register(r'goals', GoalViewSet)
urlpatterns = router.urls
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
ViewSet의 Permission을 이용함
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
## filter 기능 구현하기
id, name, is_goal_private 필드 filter 구현<br/>
filter_class로 filterset을 추가했을 때 filter가 작동하지 않는 문제가 있어서, filterset_fields로 대체함.<br/>
'lookup_expr=exact' 와 동일하게 작동함
```python
# view.py

# 이거 작동 안함
class GoalFilter(FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='icontains')
    user = filters.CharFilter(field_name='user')
    name = filters.CharFilter(field_name='name', lookup_expr='name__icontains')
    is_goal_private = filters.BooleanFilter(method='private_filter')
    color = filters.CharFilter(field_name='color')

    def private_filter(self, queryset, name, value):
        return queryset.filter(type=value)

    class Meta:
        model = Goal
        fields = ['id', 'user', 'name', 'is_goal_private', 'color']

  class GoalViewSet(viewsets.ModelViewSet):
      serializer_class = serializers.GoalSerializer
      queryset = Goal.objects.all()
      permission_classes = [AuthCheck]
      filter_backends = [DjangoFilterBackend]
      # filter_class = GoalFilter
      filterset_fields = ['is_goal_private', 'name', 'id']
```
### ex) is_goal_private 필터 적용
* 적용하지 않았을 경우
  * url : http://127.0.0.1:8000/api/goals
```json
{
    "status": 200,
    "message": "SUCCESS",
    "data": [
        {
            "id": 14,
            "user": 5,
            "name": "public 1",
            "is_goal_private": false,
            "color": ""
        },
        {
            "id": 15,
            "user": 5,
            "name": "public 2",
            "is_goal_private": false,
            "color": ""
        },
        {
            "id": 16,
            "user": 5,
            "name": "private 1",
            "is_goal_private": true,
            "color": ""
        },
        {
            "id": 17,
            "user": 5,
            "name": "private 2",
            "is_goal_private": true,
            "color": ""
        }
    ]
}
```
* 적용했을 때
  * url : http://127.0.0.1:8000/api/goals?is_goal_private=true
```json
{
    "status": 200,
    "message": "SUCCESS",
    "data": [
        {
            "id": 16,
            "user": 5,
            "name": "private 1",
            "is_goal_private": true,
            "color": ""
        },
        {
            "id": 17,
            "user": 5,
            "name": "private 2",
            "is_goal_private": true,
            "color": ""
        }
    ]
}
```

## 회고
* filterset이 작동하지 않는다. 이유를 못찾겠다.
  * django-filter를 설치했을 때, 버전이 다르다고 해서, 다른 django 버전을 적용했는데, 그 부분에서 문제가 발생한 것 같다. 정확한 이유는 모르겠고, 해결 방법도 모르겠다.
* ViewSet을 이용하여 views.py를 리팩토링하니 코드가 매우 간결해져서 좋았다. 장고가 정말 편하다는 걸 느낄 수 있었다!!

## 5주차 : DRF3 - Simple JWT
## 커스텀 User Model 사용
```python
class User(AbstractUser, BaseModel):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128, null=False)

    def __str__(self):
        return self.username
```
## Login 구현
```python
# api/view.py
class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get("id")
            password = request.data.get("pwd")

            user = User.objects.get(username=username)
            if user.password != password:
                raise
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            res = JsonResponse(custom_response(200, {"token": access_token}), status=200)
            res.set_cookie("access", access_token, httponly=True)
            return res
        except:
            return JsonResponse(custom_response(400), status=400)
```
```python
# api/url.py
urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view())
]
```
```json
{
    "status": 200,
    "message": "SUCCESS",
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY4ODM3MzYzLCJpYXQiOjE2Njg4MzU1NjMsImp0aSI6IjEzN2ViZjlmYjljMzRjM2VhMTA5ZGFhOGU0ZTA1MWI1IiwidXNlcl9pZCI6M30.09nZfqRlWMbJjwyo3GXGE2sdryWiek_mnPmFbQwstHM"
    }
}
```
viewset을 이용하는 것보다 CBV가 개인적으로 편하게 느껴져서, login은 CBV을 이용했다.
username과 password에 해당하는 유저를 찾은 후, 그 유저가 존재한다면 토큰을 전달하는 방식으로 구현했다.
## jwt 이용에 따른 유저 검증 로직 변경
```python
class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GoalSerializer
    queryset = Goal.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GoalFilter

    # 응답에 필요한 쿼리셋을 가져오기 위해 사용되는 메서드
    def get_queryset(self):
        access_token = self.request.COOKIES['access']
        payload = jwt.decode(access_token, env('SECRET_KEY'), algorithms=['HS256'])
        user_id = payload.get("user_id")
        queryset = super().get_queryset()
        return queryset.filter(user_id=user_id)
```
1. IsAuthenticated : 유저의 존재 유무를 검사
2. get_queryset : 토큰에 담긴 정보를 이용해 해당 유저의 데이터 필터링할 수 있다.
## 회고
* 지난번 filterset이 적용 안되던 문제는 filter_class -> filterset_class 로 수정하는 것으로 해결할 수 있었다.
  * filterset_class라고 적으면 파이참이 rename하라고 한다. 옆 동네 인텔리제이는 똑똑하던데, 얜 왜 이러는지 모르겠다.
* 다음에는 로그인도 viewset으로 변경해 봐야겠다.

## 6주차 : 배포환경 구축 스터디
..
