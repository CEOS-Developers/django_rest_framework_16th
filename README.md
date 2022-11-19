# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포

## 5주차 미션 : DRF3 - Simple JWT

### Q. 로그인 인증 방식은 어떤 종류가 있나요?
#### | 세션 

#### | 쿠키

#### | 토큰

### Q. JWT 는 무엇인가요?

#### 사용자 인가

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
- refresh 요청
  - body에 refresh 토큰 담아서 보냄
  ![image](https://user-images.githubusercontent.com/68186101/202855060-e9e481cb-0470-42c4-8499-81f21b3c2121.png)

#### | 로그아웃


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

### 후기

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
