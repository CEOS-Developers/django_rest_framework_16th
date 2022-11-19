# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포

## 5주차 미션 : DRF3 - Simple JWT

### Q. 로그인 인증 방식은 어떤 종류가 있나요?
#### | 세션 
- 비밀번호 등 클라이언트의 민감한 정보는 서버에, 브라우저(쿠키)엔 이에 해당하는 키값을 저장해서 인증하는 방식
- 다수 요청 시 서버의 부하가 심해질 수 있다는 단점 존재

#### | 쿠키
- 클라이언트의 쿠키에 유저 정보를 담아 주고 받는 방식
- 서버는 응답 작성 시, 쿠키에 정보 담고, 클라이언트도 요청 시 쿠키에 정보를 담아 보냄
- 쿠키의 값은 그대로 노출되어 있기 때문에 보안에 가장 취약

#### | 토큰
- 클라이언트가 서버에 접속하면 서버에서 해당 클라이언트를 인증했다는 의미로 토큰을 발급해 보내줌
- 클라이언트는 해당 토큰을 저장해 두었다가 (쿠키 등에) 서버에 요청 시, 이를 담아서 보냄

### Q. JWT 는 무엇인가요?

- 토큰 로그인 인증 방식

#### 인증 과정
- access 토큰만 사용

1. 사용자가 아이디와 패스워드를 입력하여 로그인
2. 서버는 시크릿 키(secret key)를 통해 접근 토큰(access token) 발급
3. 사용자에게 JWT 전달
4. 로그인이 필요한 API 호출 시 헤더(header)에 JWT를 담아 전송함
5. 서버에서 JWT 서명을 확인하고 시크릿 키로 JWT를 디코드하여 사용자 정보를 획득
6. 서버에서 유저를 인식하고 요청 사항에 응답함

- 토큰이 유출될 경우 누구나 정보 확인을 할 수 있어 session 방식보다 보안이 떨어짐

→ 이를 해결하고자 **`Refresh Token`**을 활용

- refresh 토큰 사용

1. 클라이언트가 ID, PW로 서버에게 인증을 요청하고 서버는 이를 확인하여 Access Token과 Refresh Token을 발급합니다.
2. 클라이언트는 이를 받아 Refresh Token를 본인이 잘 저장하고 Access Token을 가지고 서버에 자유롭게 요청합니다.
3. 요청을 하던 도중 Access Token이 만료되어 더이상 사용할 수 없다는 오류를 서버로부터 전달 받습니다.
4. 클라이언트는 본인이 사용한 Access Token이 만료되었다는 사실을 인지하고 본인이 가지고 있던 Refresh Token를 서버로 전달하여 `새로운 Access Token의 발급을 요청`합니다.
5. 서버는 Refresh Token을 받아 서버의 Refresh Token Storage에 해당 토큰이 있는지 확인하고, 있다면 Access Token을 생성하여 전달합니다.
6. 이후 2로 돌아가서 동일한 작업을 진행합니다.

#### JWT 구조

- `header`: 암호화 알고리즘, 토큰 타입
- `payload`: 전송하는 데이터, 키-값으로 구성
- `signature`: 서명, 이를 통해 토큰의 진위 여부 확인 가능

#### JWT 인증 과정 도식화
![image](https://user-images.githubusercontent.com/68186101/202857327-37d63827-ffed-4235-a40a-41f9c6391fff.png)

### JWT 로그인 구현하기

#### | 커스텀 User 모델 만들기

- User를 관리하는 account 앱 생성
- User 모델 생성 (id & password로 로그인 할 수 있는)
- `settings/base.py` 에 `AUTH_USER_MODEL = 'account.User'` 추가

##### Reference
[초기 구조 잡기](https://wikidocs.net/10294)

[전반적 코드 참고](https://velog.io/@iedcon/AbstractBaseUser%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-Django-%EC%BB%A4%EC%8A%A4%ED%85%80-%EC%9C%A0%EC%A0%80-%EB%AA%A8%EB%8D%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0)

#### | JWT settings
- simple jwt 설치
```shell
pip install djangorestframework-simplejwt
```
- settings.py 수정
```shell
 INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
    ...
]

REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    ...
}

# JWT setting
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'TOKEN_USER_CLASS': 'account.User',  # custom user model

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}
```
- `ACCESS_TOKEN_LIFETIME` : access token 유효 기간
- `REFRESH_TOKEN_LIFETIME` : refresh token 유효 기간
- `ROTATE_REFRESH_TOKENS` : True이면, refresh 요청 시 새로운 access token과 refresh token 반환
- `BLACKLIST_AFTER_ROTATION` : True이면, 더 이상 필요없는 토큰(로그아웃)이나 악의적으로 탈취된 token을 서버에서 사용할 수 없도록 관리해줌

#### | JWT REST API
- 회원가입 `account/register/`
- 로그인 `account/login/`
- 인가 확인 `account/auth/`
- Refresh 요청 `account/auth/refresh/`
- 로그아웃 `account/logout`


#### | 회원가입
- 회원가입 성공 `201 OK`
  ![image](https://user-images.githubusercontent.com/68186101/202844328-1654ef49-d879-4bc7-8d18-4c3956e543fd.png)
- 이미 존재하는 계정 `400`
  ![image](https://user-images.githubusercontent.com/68186101/202847722-fc05710b-58b9-4fbf-80b3-85c8e8fa78d9.png)


#### | 로그인 
- 로그인 성공 `200 OK`
  ![image](https://user-images.githubusercontent.com/68186101/202847927-42b6cf85-b497-4cd6-a962-00a16e9b6233.png)
- 존재하지 않는 계정 `400`
  ![image](https://user-images.githubusercontent.com/68186101/202847958-e54e39d9-9d00-4af0-8d64-e5113985981d.png)
- 비밀번호 오류 `400`
  ![image](https://user-images.githubusercontent.com/68186101/202847978-1609de91-2306-42be-838b-25348d1ac352.png)


예외는 serializer에서 raise를 발생시켜서 처리


#### | Refresh Token 발급
- 라이브러리 내장 뷰 활용 `TokenRefreshView.as_view()`
- body에 refresh 토큰 담아서 보냄
- refresh 요청 성공
  ![image](https://user-images.githubusercontent.com/68186101/202855060-e9e481cb-0470-42c4-8499-81f21b3c2121.png)

- 유효하거나 만료된 토큰일 경우
  ![image](https://user-images.githubusercontent.com/68186101/202855548-bf61de7b-54cc-418d-82e8-f3a0461c350e.png)


#### | 로그아웃
- 쿠키에 저장된 access_token, refresh_token을 삭제
- 로그아웃 완료
  ![image](https://user-images.githubusercontent.com/68186101/202856387-66761b27-068c-4224-a515-e0503a97207a.png)

#### | 인가
- 토큰을 복호화해서 검증한 다음, 유저 id 추출해서 권한 확인
- 유저 확인 성공
  ![image](https://user-images.githubusercontent.com/68186101/202866630-7e3c9a12-a5b3-410c-b0fb-93f5e2a5a885.png)

- 토큰 예외
  - 토큰 없음
    ![image](https://user-images.githubusercontent.com/68186101/202866663-49ebf46c-8f4f-4a97-b86b-962181a6c670.png)

  - 토큰 유효하지 않음
    ![image](https://user-images.githubusercontent.com/68186101/202866653-7778368e-6d86-4916-8f4d-80412f4bf2a0.png)

  - 토큰 기간 만료


### Issue
#### Custom User Model Migration 할 때
- 새로운 사용자 모델로 마이그레이션 하려 할 때 아래 오류 발생
  `(fields.E301) Field defines a relation with the model 'auth.User', which has been swapped out.
        HINT: Update the relation to point at 'settings.AUTH_USER_MODEL'.`
- 새로 바뀐 유저 모델을 얻어와야 했던 거였음 [[해결 링크]](https://stackoverflow.com/questions/55780537/how-to-fix-field-defines-a-relation-with-the-model-auth-user-which-has-been-s)
  ```python
  from django.contrib.auth import get_user_model
  User = get_user_model()
  ```
### 새롭게 안 사실
- simple JWT에서는 token 생성 시 필요한 secret key에 Django 프로젝트마다 사용하는 secret_key를 기본으로 이용함

### 후기
- 일단 node에서 express로 jwt 인증/인가 구현할 때보다 코드가 훨씬..예쁘다..
- 그럼에도 중복 코드들이 있어서 리팩토링 하고 싶다
- 장고는 편리하게 쓸 수 있는 라이브러리들이 많이 있어서 쉬워보이다가도 막상 제대로 쓰려면 커스텀을 해야 하니 호락호락하지 않은 프레임워크라는 것을 또 느꼈다..
- 로그아웃 할 때도, 토큰 확인이 먼저 필요할 거 같다
- node에서는 인가 확인을 미들웨어로 만들어서 다른 api에서도 쉽게 사용이 가능했는데, 장고에서도 그런 방법이 있는지 알아보고 싶다

## 4주차 미션 : DRF2 - API View & Viewset & Filter

### DRF API View 의 CBV 으로 리팩토링하기
- CBV로 리팩토링하면서 클래스 내 메서드를 생성해서 사용함으로써 코드가 더 깔끔해진 것 같다.
- `get_object(self, id)` 메서드를 만들어서 오브젝트를 DB에서 얻어오고, 없으면 바로 404를 반환하도록 했다.


### Viewset으로 리팩토링하기
- `ModelViewSet`의 기능들 + HTTP Method + URL
  - 목록 얻기 : `list()` `GET todos/`
  - 특정 데이터 얻기 : `retrieve()` `GET todos/<int:pk>`
  - 데이터 생성 : `create()` `POST todos/`
  - 데이터 수정 (완전) : `update()` `PUT todos/<int:pk>`
  - 데이터 수정 (일부) : `partial_update()` `PATCH todos/<int:pk>`
  - 데이터 삭제 : `destroy()` `DELETE todos/<int:pk>`
  
  
- `as_view()` 함수 활용하기
```py
# views.py

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import ToDo
from .serializers import ToDoSerializer

class TodoViewSet(ModelViewSet):
    serializer_class = ToDoSerializer
    queryset = ToDo.objects.all() 

todo_list = TodoViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

todo_detail = TodoViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})
```
```py
# urls.py

from django.urls import path, include
from . import views

urlpatterns = [
    path('todos/', views.todo_list),
    path('todos/<int:pk>/', views.todo_detail),
]
```
- `router` 활용하기
```py
# views.py

from rest_framework.viewsets import ModelViewSet
from api.models import ToDo
from api.serializers import ToDoSerializer


class TodoViewSet(ModelViewSet):
    serializer_class = ToDoSerializer
    queryset = ToDo.objects.all()

```
```py
# urls.py

from rest_framework import routers
from .views import TodoViewSet

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)  # register()함으로써 두 개의 url 생성

urlpatterns = router.urls
```


### filter 기능 구현하기
```py
def list(self, request, *args, **kwargs):
    query_params = request.query_params
    self.queryset = self.get_queryset().filter(content__icontains=query_params.get('content'))
    return super().list(request, *args, **kwargs)
```
- goal 필터

![image](https://user-images.githubusercontent.com/68186101/201207545-7e1fc0d4-34d6-4e93-8249-7cd94e5647b4.png)


- todo content에 특정 문자 포함한 거 찾기

![image](https://user-images.githubusercontent.com/68186101/201209178-a2735641-0b9d-4330-b30f-4fbc3d4825a8.png)


#### filterset 활용

```py
class TodoFilter(FilterSet):
    content = filters.CharFilter(field_name='content')
    is_done = filters.BooleanFilter(field_name='is_done')

    class Meta:
        model = ToDo
        fields = ['content', 'is_done']
```


- content필드와 is_done필드 필터링하기

![image](https://user-images.githubusercontent.com/68186101/201251538-d79fc63f-5dbc-44ec-977f-d8a5b0739cb4.png)



### Issue
- delete 요청 시 에러 해결 ! 
  - 에러 : DB에서 삭제는 되는데, Response에서 오류.
  ```
  TypeError: __init__() missing 1 required positional argument: 'data'
  ```
  - 해결
    - JsonResponse 대신 Response로 보내니 해결
- 슬래시 안 붙여서 오류.. 
  - 에러 
    ```
    RuntimeError: You called this URL via PATCH, but the URL doesn't end in a slash and you have APPEND_SLASH set. Django can't redirect to the slash URL while maintaining PATCH data. Change your form to point to localhost:8000/api/todos/4/ (note the trailing slash), or set APPEND_SLASH=False in your Django settings.
    ```
  - 해결
    - api 요청 주소 마지막에 '/'를 안 넣어서 생긴 오류였다.. 
    https://codingdojang.com/scode/377
- filtering 할 때, 외래키 관련 오류
  - 에러
  ```
  django.core.exceptions.FieldError: Related Field got invalid lookup: icontains
  ```
  - 해결
    - 외래키는 칼럼 이름에 id가 붙어서 나는 오류였다. 이름 사이에 `__id__`를 넣으니 해결!
    - `goal__icontains` -> `goal__id__icontains`


### 후기 💪
- DB 테이블을 많이 수정했다. 마이그레이션 과정에서 꼬여서 결국 DB 다시 생성해서 해결했는데, 실제 협업하면 이럴 수 없으니까 얼른 마이그레이션에 익숙해져야겠다............
- CBV로 리팩토링 하는 과정에서 기존에 잘 처리하지 못했던 예외처리까지 하게 되었다! 
- viewset... 정말정말 간편하다.. 대박 신세계다 ✨✨✨✨✨✨
- filtering 할 때는 api 요청 주소 마지막에 슬래시('/') 넣으면 안된다. (왜 그러지?) 
- fileterset 메서드 구현에 대해 공부 필요


## 3주차 미션 : DRF1 - Serializer 및 API 설계

### 모델 선택 및 데이터 삽입
```shell
>>> from api.models import *
>>> category = Category.objects.create(user_id=1, name='playing')
>>> category.save()
>>> todo = ToDo.objects.create(user_id=1, category_id=1, content='math', is_done=False, is_repeat=False)
>>> todo = ToDo.objects.create(user_id=1, category_id=2, content='practice drum', is_done=False, is_repeat=False)
>>> todo.save()
>>> todo = ToDo.objects.create(user_id=1, category_id=1, content='math', is_done=False, is_repeat=False)
>>> todo.save()
>>> todo = ToDo.objects.get(id=4)
>>> todo.content
'math'
>>> todo.content = 'english'
>>> todo.save()
```
- 카테고리 (category)

![image](https://user-images.githubusercontent.com/68186101/194684633-5fd1cc44-a1a3-4291-b054-7266cd018572.png)

- 해야할 일 (todo)

![image](https://user-images.githubusercontent.com/68186101/194684607-14210892-95d6-49e0-83f7-bfc2e2702a20.png)

### 모든 데이터 가져오는 API
- URL: `api/todo/` 
- METHOD: `GET`

![image](https://user-images.githubusercontent.com/68186101/194711986-bd70146f-ef73-47f7-a84f-9752b0fed747.png)
![image](https://user-images.githubusercontent.com/68186101/194712063-5ea9c06a-9974-4214-9dae-468d34d76d12.png)


### 특정 데이터 가져오는 API
- URL: `api/todo/<int:pk>/`
- METHOD: `GET`

![image](https://user-images.githubusercontent.com/68186101/194712790-472e0e3b-044c-40bf-9030-b730c57d4902.png)


### 새로운 데이터 create 하는 API
- URL: `api/todo/`
- METHOD: `POST`
- BODY
  ```json
  { "user" : "유저번호", 
    "category" : "카테고리 번호", 
    "content" : "todo 내용", 
  } 
  ```
![image](https://user-images.githubusercontent.com/68186101/194712199-0f38d706-2b16-4d5d-8116-6c94aa1c0ac1.png)

  

### 데이터 삭제하는 API
- URL: `api/todo/<int:pk>`
- METHOD: `DELETE`

- 에러
```
TypeError: __init__() missing 1 required positional argument: 'data'
```


### 데이터 업데이트하는 API
- URL: `api/todo/<int:pk>`
- METHOD: `PUT`
  ```json
  { "필드명" : "업데이트할 필드값", 
     ...
  } 
  ```
  
![image](https://user-images.githubusercontent.com/68186101/194713453-c7faa5e5-c0fd-4ffb-99b4-33e2df020a22.png)
  
  
### Issue
- 모든 데이터 얻는 GET 요청에서 아래 에러가 났었다 😥
  - 에러 메시지
  ```py
  TypeError: In order to allow non-dict objects to be serialized set the safe parameter to False.
  ```
  -> 구글링 해서 해결책을 찾은 결과..
  기존에 views.py에서 JSON 전달하는 부분에 safe=False를 추가해주니 해결되었다
  ```py
  return JsonResponse(serializer.data, safe=False)
  ```
- 특정 데이터 얻는 GET 요청에서 아래 에러가 났었다
  - 에러 메시지
  ```py
  TypeError: 'ToDo' object is not iterable
  ```
  -> 알고보니, 객체가 하나인데, serializer를 해줄 때, `many=True` 속성을 넣어서 에러가 났던 거 같다! 이걸 빼니까 해결되었다. list가 아닌데 list인척 하려니 당연히 에러가 나지..! 난 바보다..
  
- Forbidden (CSRF cookie not set.) 오류
[해결 블로그](https://velog.io/@langssi/django-Forbidden-CSRF-cookie-not-set.-%EC%98%A4%EB%A5%98-%ED%95%B4%EA%B2%B0
)

- 데이터 Update하는 PUT 요청 시 아래 에러 났었음
  - 에러 메시지
  ```
  TypeError: __init__() missing 1 required positional argument: 'data'
  ```
  -> 필드 값을 다 안채워줘서 그런 거 같다. 필드 값 다 채워주니 에러는 해결. 
  ❗ 그런데 그럼 매번 update마다 모든 필드를 채운 다음에 변경값만 변경해서 보내줘야 하는건가..? -> 알아볼 필요 !!


### 후기 💪
api설계의 난이도는 어렵지 않았지만, 역시 늘 다른 언어를 배우고 새로운 프레임워크를 배우고 응용하는 건 어려운 일인 것 같다!!!! 장고로 api를 직접 구현하며 에러도 많이 보고,,해결하고,,!! 이번 기회를 통해 장고랑 더 많이 친해진 거 같아서 기분이 좋다 💘😎


## 2주차 미션: DB 모델링 및 Django ORM

### 투두메이트 서비스 설명

![todo_mate](https://user-images.githubusercontent.com/68186101/193458056-025adc6e-1a80-4024-8829-8353b08ef34f.png)
#### 오늘 해야 할 일을 기록하고, 친구들과 공유함으로써 더욱 동기를 부여하는 서비스
- 해야 할 일을 **자신의 분류(목표)별**로 나눠서 기록할 수 있음
- **분류(목표)별로 색**을 지정할 수 있음. 할 일을 완료하면 분류에 맞는 색이 채워져서 **채우는 재미**가 있음
- 매일 하는 일 등 **반복적으로 하는 일**에 대해서도 따로 **간편하게 설정 가능**
- **오늘의 일기**도 간략하게 기록할 수 있음 (기분도 이모지로 기록 가능)
- 친구와 함께 투두를 공유함으로써 **서로 동기부여**도 하고, 친구의 할일을 **응원하는** 이모지 기능도 있음

<br></br>

### 투두메이트 모델링 결과
![db_erd](https://user-images.githubusercontent.com/68186101/193458050-3a930229-6e60-4452-847a-ce5c80592d7f.png)
1. 유저는 목표를 여러 개 세울 수 있다. (1 : N)
2. 유저는 할 일을 여러 개 만들 수 있다. (1 : N)
3. 목표는 할 일을 여러 개 가질 수 있다. 하나의 할 일은 한 목표에 대응된다. (1 : N)
4. 친구 관계 (N : M)





<br></br>

### ORM 이용해보기

- 파이썬 쉘 들어가기
```shell
python manage.py shell
```

1. **데이터베이스에 해당 모델 객체 3개 넣기**
```shell
>>> from api.models import *
>>> from auth.models import *
>>> user = User.objects.create()
>>> user.save()
>>> user = Profile.objects.create(nickname='ori', bio='hello', user_id=1) 
>>> user.save()
>>> category = Category.objects.create(user_id=1, name='homework')
>>> category.save()
>>> todo = ToDo.objects.create(user_id=1, category_id=1, content='coding', is_done=False, is_repeat=False)
>>> todo.save()

```
![orm_1](https://user-images.githubusercontent.com/68186101/193458053-485653b1-2824-4bfa-9b3d-5a16940471fc.png)

2. **삽입한 객체들을 쿼리셋으로 조회해보기 (단, 객체들이 객체의 특성을 나타내는 구분가능한 이름으로 보여야 함)**

![orm_2](https://user-images.githubusercontent.com/68186101/193458054-cc617145-7745-4d3c-bdb4-3f685cb818c0.png)

3. **filter 함수 사용해보기**

![orm_3](https://user-images.githubusercontent.com/68186101/193458055-6c073b82-d5f3-4f92-aaa9-ac3915ca1d56.png)

<br></br>

### 새롭게 알게된 점

- `TextField()` 와 `CharField()` 의 차이
</br>: 최대 길이의 정의가 필요할 경우 주로 CharField() 사용

- 장고는 모델에서 기본 키 자동으로 만들어 준다.
- 같은 테이블에서 외래키로 가져올 시, `related_name=''` 설정을 꼭 해줘야 한다
- 모델 설정 시, db 관계를 명령어를 통해 쉽게 설정할 수 있음 (`OneToOneField`, `ManyToManyField`, ...)
<br></br>

### 회고

1주차 때는 문서를 따라하며 예제를 해서 확 와닿지 않았는데, 이번에 직접 모델링도 해보며 장고에서 모델을 어떻게 사용하는지 확 와닿은 것 같다!!

그런데 아직 구글링 없이는 코드를 못짜겠어서 훨씬 더 공부를 많이 해야겠다.. 💪💪🔥🔥

그리고 node에서는 ORM을 사용할 때 설정해줘야 하는 게 더 많은 느낌인데 장고는 ORM이 아예 내장(?) 된 느낌이라 훨씬 편한 것 같다 ✨

<br></br>

### 더 알아보고 싶은 것

- migrate 했을 시 생기는 장고 관련 테이블에 대해 <br></br>
![db_init_table](https://user-images.githubusercontent.com/68186101/193458052-d6127c0d-dabc-437f-b52b-d6220f61e8e7.png)

- 기본 키 자동으로 만드는 거 커스텀 할 수 있는지에 대해
