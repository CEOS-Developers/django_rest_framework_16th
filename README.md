# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포


## 2주차 미션: DB 모델링 및 Django ORM

### todo mate ✓
오늘 하루 해야할 일과 있었던 일을 쉽고 예쁘게 기록할 수 있는 어플리케이션

**주요 기능 정리**
- 목표 설정, 목표별 색상 관리
- 목표 당 할일 목록 분류
- 할일 보관함으로 이동
- 원하는 시간에 할일 시간 알림
- 오늘 하루 일기 적기
- 일기에 대표 이모지 설정
- 친구 계정 팔로잉

### DB 설계
<img width="534" alt="image" src="https://user-images.githubusercontent.com/68368633/193413230-b0c15e84-1512-43a1-994d-3deb28c2d6f2.png">

- todo의 color나 diary의 emoji는 개발하게 된다면 프론트 측과 합의해서 결정해야 할 것 같다.

- follower/following의 설계가 저런 식이 아닐 것 같다.


models.py 작성 끝나면 migration!
```
python manage.py makemigrations
python manage.py migrate
```
### ORM 이용해보기
**python shell 들어가기**
```angular2html
python manage.py shell
```
1. 데이터베이스에 해당 모델 객체 3개 넣기
![image](https://user-images.githubusercontent.com/68368633/193413199-df894bcb-ec59-43fd-afe4-76d3b4659050.png)
2. 삽입한 객체들을 쿼리셋으로 조회해보기 (단, 객체들이 객체의 특성을 나타내는 구분가능한 이름으로 보여야 함)
![image](https://user-images.githubusercontent.com/68368633/193413193-25847923-d905-49bc-8027-b88335d7fbe9.png)
3. filter 함수 사용해보기

  ![image](https://user-images.githubusercontent.com/68368633/193413421-85045bee-7289-46f7-88f5-1bada10195b6.png)


### 에러 해결
- ModuleNotFoundError: No module named 'environ'

  ```
  $ pip install django-environment
  ```

- NameError: name '_mysql' is not defined
  
  django에서 mysql 개발할 때 가끔 발생하는 에러라고 한다. mysql을 reinstall해보고 안된다면 아래와 같이 pymysql로 충돌 및 호환 문제 잡기!
  ```
  $ pip install pymysql
  ```
  setting.py 역할을 하는 settings/base.py에 아래 코드 추가
  ```angular2html
  import pymysql
  
  pymysql.install_as_MySQLdb()
  ```
- RuntimeError: 'cryptography' package is required for sha256_password or caching_sha2_password auth methods

  ```
  $ pip install cryptography
  ```
- MySQL django.db.utils.OperationalError : (1045, " 'root'@ 'localhost'사용자에 대한 액세스가 거부되었습니다 (암호 사용 : YES)")
  
  settings.py의 DATABASE_PASSWORD 재확인

### 새로 알게된 점
- OneToOneField
  
  일대일 관계로 unique=True를 이용해서 만든 ForeignKey와 비슷하지만 단일 객체를 직접 리턴하는 **역참조**라는 점이 다르다.

- DateField에서 default=datetime.date.today()를 썼더니 아래와 같은 경고가 나타났다.

  ```
  It seems you set a fixed date / time / datetime value as default for this field. This may not be what you want. If you want to have the current date as default, use `django.utils.timezone.now`
  ```
  
  그래서 from django.utils import timezone를 추가해서 timezone.localtime() 형식으로 바꾸긴 했는데 왜 이렇게 해야 하는지 잘 모르겠다.

### 느낀 점
DB 설계를 너무 오랜만에 해봐서 감이 잘 안잡혔다. create/update 시간도 필드로 추가했어야 했는데 잊었다. 그리고 following/follower를 구조 상 어떻게 표현해야 할지 모르겠어서 내 생각대로 해봤는데 아마 틀린 것 같다. 🥲
책 좀 읽고 공부해야겠다!

---

## 3주차 미션 : DRF1 - Serializer 및 API 설계
### 데이터 구조 수정
![image](https://user-images.githubusercontent.com/68368633/194756523-96f4e2dc-0d56-4034-ab5f-37bd5158af3e.png)


2주차 과제 코드리뷰 때 말씀해주셨던 점들을 반영하여 구조를 수정했다.
```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
```
BaseModel Class를 만들어 다른 모델에서도 반복적으로 필요한 변수들을 추가하여 관리하는 방식으로 변경했다. 

### 데이터 삽입
![image](https://user-images.githubusercontent.com/68368633/194756547-de480898-ee47-44fc-b3f3-aab6d0445f66.png)
![image](https://user-images.githubusercontent.com/68368633/194756558-7869d199-9137-4075-bfc3-9023d9e2ed24.png)

- 추가된 데이터 
  - Category: study, play 
  - Todo: django study, code review, lets go sinchon
- mysql로 확인

  ![image](https://user-images.githubusercontent.com/68368633/194756567-913be689-274e-47dc-831e-40f77d278c5b.png)


### 모든 데이터를 가져오는 API
- URL: api/todo
- METHOD: GET
  ![image](https://user-images.githubusercontent.com/68368633/194756576-9ff73e4f-553e-430c-acd3-4c20f2a36ab2.png)

### 특정 데이터를 가져오는 API
- URL: api/todo/<int:pk>
- METHOD: GET
  ![image](https://user-images.githubusercontent.com/68368633/194756582-31c62d19-e657-4588-89e9-1c321cfc64cc.png)

### 새로운 데이터를 create하도록 요청하는 API
- URL: api/todo
- METHOD: POST
- BODY
  ```json
  {
    "user": "유저 ID",
    "category": "카테고리 ID",
    "content": "TODO 내용"
  }
  ```
  ![image](https://user-images.githubusercontent.com/68368633/194756593-40851b84-f09b-4ad7-beb0-acc0e91a88bb.png)

  deadline을 지정하지 않아도 괜찮지만 models.py에서 field와 default의 데이터 타입을 다르게 설정하여 에러가 나 이번에만 설정해주었다. 추후에 수정 예정
  
### 특정 데이터를 삭제 또는 업데이트 하는 API
#### 삭제
- URL: api/todos/< int:pk >
- METHOD: DELETE

  <img width="1006" alt="image" src="https://user-images.githubusercontent.com/68368633/194756628-347713d8-611a-4581-b932-de1a2ce61ce7.png">
  
  삭제 결과

  ![image](https://user-images.githubusercontent.com/68368633/194756647-b63253ce-22e1-40ff-8bd6-d31a51a96ee7.png)

#### 업데이트
- URL: api/todo/< int:pk >
- METHOD: POST
- BODY
  ```json
  {
    "user": "유저 ID",
    "category": "카테고리 ID",
    "수정을 원하는 필드"
  }
  ```
  ![image](https://user-images.githubusercontent.com/68368633/194756666-0021258b-acea-46e0-9609-809a3be2679c.png)

  user와 category를 body 추가하지 않고 api를 요청하였더니 필수값이라고 에러가 났다. 안해도 상관 없는 것으로 아는데 확인 필요!
  ```python
  serializer = TodoSerializer(instance=todo, data=data, partial=True)
  ```
  serializer에 partial=True을 추가하여 해결
### 에러 해결
- BaseModel의 created_at

  ![image](https://user-images.githubusercontent.com/68368633/194756675-2448c930-f5da-4206-a66e-745fe9fb1402.png)

  이때 created_at에 그냥 auto_now_add=True만 지정해주면 다음과 같이 default를 추가하라는 메시지가 나온다.

  ![image](https://user-images.githubusercontent.com/68368633/194756685-8af0968f-3cc6-4c9d-961d-675c1b432ce0.png)

  그래서 default를 지정해주면 둘 중에 하나만 쓰라고 에러 메시지가 출력되어 null=True을 추가하여 우선 해결해주었다.

- DELETE
  DELETE 요청 시에 발생
  
  ![image](https://user-images.githubusercontent.com/68368633/194756693-42741d26-d788-48d3-95ce-72a41fea5be6.png) 
  ```
  TypeError: __init__() missing 1 required positional argument: 'data'
  ```
  에러가 나지만 DB를 확인해보면 어찌됐든 지워져 있었다. 구글링해봐도 잘 모르겠어서 더 찾아보고 수정해야 한다.
  
  &rarr; JsonResponse를 Response로 수정하여 해결!

- safe
  ```
  TypeError: In order to allow non-dict objects to be serialized set the safe parameter to False.
  ```
  GET 요청 시에 자꾸 발생했던 에러이다. views.py에서 각 api의 리턴 값에 safe를 추가해주면 된다.

  ```python
  return JsonResponse(serializer.data, safe=False)
  ```


### 회고
백엔드 개발자가 된 기분! 너무 재밌었다 🤓 처음에 urls.py에 내가 짠 todo path를 추가해주는 것을 상위 url conf에서 하고 있었다.
이런 바보 같은 실수는 도대체 언제 끝나는건지..

데이터를 기본 테이블을 만들어서 상속 받는 관계로 변경하고 나서 코드를 짜려고 하니까 serializer에서도 어떻게 해야 하는 것인가 고민이 있었다.
그리고 세션 때 알려주신 SerializerMethodField를 추가해서 좀 하고 싶었는데 에러가 생겨서 우선 주석처리 해놨다.😢

이번 과제에서 모르는 부분들을 많이 발견해서 답답하기도 했지만 공부할 것들을 찾은 것 같아 좋았다!

----
## 4주차 : DRF2 - API View & Viewset & Filter
#### 저번 주차와 비교했을 때 달라진 점들:
- url 형태: todo/ &rarr; todos/
- 특정 데이터 업데이트 메소드:  PUT &rarr; PATCH
- BaseModel에서 삭제 여부와 시기를 관리하던 is_deleted와 deleted_at 필드 중 is_deleted 제거
- migration 파일들 git에 추가

### DRF API View 의 CBV 으로 리팩토링하기
기존에 FBV(Function-Based View)로 코딩했던 내용을 CBV(Class-Based View)로 수정하였다.

views.py refactoring 전/후
```python
# FBV
@csrf_exempt
@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.filter(deleted_at=None)
        serializer = TodoSerializer(todos, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
```
```python
# CBV
class TodoList(APIView):
    def get(self, request):
        todos = Todo.objects.filter(deleted_at=None)
        serializer = TodoSerializer(todos, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
```
urls.py refactoring 전/후
```python
# FBV
urlpatterns = [
    path('todos/', views.todo_list, name="todo_list"),
    path('todos/<int:pk>', views.todo_detail, name="todo_detail"),
]
```
```python
# CBV
urlpatterns = [
    path('todos/', TodoList.as_view()),
    path('todos/<int:pk>', TodoDetail.as_view()),
]
```
### Viewset으로 리팩토링하기
views.py refactoring 후
```python
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
```
urls.py refactoring 후 (Router 사용하여 url mapping)
```python
router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = router.urls
```
### filter 기능 구현하기
- 특정 user filtering 
- content에 특정 문자열 포함되는지 판별하여 filtering
```python
class TodoFilter(FilterSet):
    user = filters.CharFilter(method='user_filter')
    content = filters.CharFilter(field_name='content', lookup_expr='icontains')

    class Meta:
        model = Todo
        fields = ['user', 'content']

    def user_filter(self, queryset, user, value):
        filtered_queryset = queryset.filter(**{
            user: value,
        })
        return filtered_queryset


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter
```
#### user filter
  url: /api/todos/?user=''

  ![image](https://user-images.githubusercontent.com/68368633/201473291-50ef8953-ebfe-4980-a9a3-5439e6baa203.png)


#### content filter
  url: /api/todos/?content=''

  ![image](https://user-images.githubusercontent.com/68368633/201473301-102846c0-e979-4a5d-b0d2-7c587dc0e1f4.png)


#### user & content filter
  url: /api/todos/?user=''&content=''

  ![image](https://user-images.githubusercontent.com/68368633/201473308-fa88508b-748b-4177-ad81-0793ffb6c81e.png)


### 에러 해결
- Field 삭제 에러
  
  ![image](https://user-images.githubusercontent.com/68368633/201473317-7ea270db-b8f9-48fb-bf30-e6702e066c83.png)


  is_deleted 필드를 삭제하고 deleted_at으로만 삭제 여부와 시기를 관리하도록 models.py를 수정하였다. 
  파일 수정 후에 마이그레이션을 했는데도 DB에는 반영이 되지 않아 아직 필드가 남아있어 발생하는 오류였다. 
  mysql로 들어가 <code>ALTER TABLE `테이블명` DROP `컬럼명`;</code>로 필드를 하나하나 삭제하여 해결

- Todo TypeError
  
  ![image](https://user-images.githubusercontent.com/68368633/201473320-ec0054ea-5634-4125-b587-821f7c76eda5.png)


  특정 데이터를 확인할 때 발생했던 에러로 get_object_or_404를 objects.filter로 수정하여 해결

### 회고
과제하려고 보니까 분명 월요일까지만 해도 있던 migration file들이 다 날라가서 간담이 서늘했다. git에 migration file들을 굳이 올릴 필요가 있나..? 싶어서 안올렸었는데 이제 꼬박꼬박 올려야겠다.
파일들이 다 날라갔어도 DB 연결은 잘 되어있고 migration 기록들을 보면 아직 다 있는데 왜 내 로컬에서만 사라진건지 정말 의문 🤔
그리고 피드백을 받고서 코드를 수정했던 부분들이 예상치 못하게 에러가 나서 왜 그러는건지도 감이 안잡힌다. 우선 주먹구구식으로 해결..

CBV와 ViewSet 모두 처음 사용해보는데 정말 신세계였다. 특히 ViewSet 어떻게 이렇게 간편할 수가..! 근데 오히려 처음 배울 때 ViewSet으로 했으면 어떻게 작동하는건지 몰라서 헷갈렸을 것 같다.
filterset도 익숙하지가 않아서 deleted_at이 Null이 아닌 데이터들만 가져오는 필터 기능을 추가하고 싶었는데 만들다가 포기했다 🙃
어쨌든 너무너무 편한 기능들을 알게 되어서 재밌었다!

----
## 5주차 : DRF3 - Simple JWT
### 로그인 인증 방식에는 어떤 것이 있을까?
+) 인증을 해야하는 이유
  
  HTTP는 기본적으로 stateless, connectionless하기 때문에 모든 요청(Request)이 이전 요청과 독립적으로 다뤄진다.
  요청이 끝날 때마다 서버는 유저에 대한 정보를 잊어버리게 되기 때문에 요청 시마다 클라이언트는 서버에 인증을 해야 한다.

#### Header
HTTP Request Header에 인증 수단인 비밀번호를 직접 넣는 방식이다.
보통 서버로 HTTP 요청을 할 때 암호화를 하지 않기 때문에 보안적으로 매우 치명적이다.
만약 해커가 HTTP 요청을 볼 수 있다면 사용자의 계정 정보를 쉽게 알 수 있다.

- 장점
  - 인증 테스트 때 사용 가능
- 단점
  - 보안 매우 취약
  - 요청 시마다 서버에 ID, PW 대조 필요
-----
#### Session, Cookie
*Session: 서버가 가지고 있는 정보
*Cookie: 사용자에게 발급된 세션을 열기 위한 열쇠(Session ID)

Session, Cookie 방식은 Session ID를 만드는 세션 저장소를 사용하는 방식이다.
Session ID는 로그인을 했을 때 사용자의 정보를 저장하는 것으로 HTTP Header에 실려 사용자에게 보내진다.
사용자는 보관하고 있던 쿠키를 인증이 필요한 요청에 넣어 보내고 서버는 세션 저장소에서 쿠키와 기존 정보를 비교하여 인증한다.
세션을 사용하여 인증하여 책임을 서버가 지게 한다고 볼 수 있다.(사용자보다는 서버 해킹이 더 어렵기 때문)

- 장점
  - Header 방식과는 다르게 HTTP 요청이 노출되더라도 안전하다. 사용자의 정보는 세션 저장소에 저장되고 HTTP 요청에 들어있는 쿠키 자체는 유의미한 정보가 없기 때문이다.
  - 사용자는 각각 고유한 Session ID를 발급 받아 회원 정보 확인이 매번 필요하지 않기 때문에 서버 자원에 접근이 용이하다.
- 단점
  - Session Hijacking 공격 가능
    세션을 가로채서 별도의 인증 작업 없이 세션을 통해 통신을 계속하는 행위를 말한다. HTTPS 프로토콜을 사용하거나 세션에 만료 시간을 설정하는 방식으로 해결 가능하다.
  - 세션 저장소를 사용하기 때문에 별도의 저장공간이 필요하다.
-----
#### Access Token (JWT)
- 장점
  - 세션 쿠키 방식과 달리 저장소를 사용하지 않기 때문에 별도의 저장공간이 필요하지 않다.
  - Google, Facebook과 같은 다양한 토큰 기반 서비스로 관련 기능을 확장하기 용이하다
  - 서명에는 송신자와 송신한 정보들에 대한 내용이 포함되어 있어 서버에서 데이터 조작 및 변조 여부를 알아낼 수 있다.
- 단점
  - Token이 발급되면 만료 시간 전까지 계속 사용할 수 있기 때문에 세션 쿠키 방식과 같이 해커가 토큰을 가로채서 사용할 수 있다.
    Refresh Token을 발급하여 사용하는 방식으로 해결 가능하다.
  - Payload는 따로 암호화하지 않기 때문에 담을 수 있는 정보가 제한적이다.
  - Token의 길이가 길어 요청이 많아질수록 서버의 자원 낭비가 생긴다.
-----
#### Access Token, Refresh Token
*Refresh Token: Access Token과 같은 형태의 JWT이다. Access Token보다 긴 유효기간을 가지며 Access Token 만료 시에 새로 발급을 도와준다.

Refresh Token을 사용하여 사용자가 자주 로그인을 해야 하는 상황이나 장기간 로그인했을 때 발생하는 보안적 문제점들을 해결하였다.

- 장점
  - 유효 기간이 더 짧기 때문에 Access Token만 단독으로 사용하는 경우보다 보안적으로 더욱 안전하다.
- 단점
  - 구현이 복잡하다.
  - 서버의 자원 낭비가 생긴다.
-----
#### OAuth 2.0
*OAuth 2.0(Open Authorization): 인증을 위한 개방형 표준 프로토콜
- 장점
  - 직접 타사 사용자의 정보를 입력하는 것보다 안정적이다.
  - 회원 정보뿐만 아니라 기타 API에 대한 정보에도 접근이 가능하다.
- 단점
  - 구현이 매우 복잡하다.


[참고링크1](https://velog.io/@gusdnr814/%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%9D%B8%EC%A6%9D-4%EA%B0%80%EC%A7%80-%EB%B0%A9%EB%B2%95)

[참고링크2](https://tansfil.tistory.com/58?category=475681)

[참고링크3](https://baked-corn.tistory.com/29)


### JWT(JSON Web Token)란 무엇인가?
통신 양자간의 정보를 JSON 형식을 사용하여 안전하게 전송하기 위한 방법이다.
JWT는 일반적으로 인증(Authentication)과 권한부여(Authorization)에 사용되는데 이때 필요한 정보들을 암호화시킨 JSON 토큰이다.
인증 절차를 거쳐서 서버에서 JWT를 발급해주면 이를 잘 보관하고 있던 클라이언트가 API 사용과 같을 때에 서버에 JWT를 제출하여 인가를 받을 수 있다.

JSON 데이터를 Base64 URL-safe Encode 를 통해 인코딩하여 직렬화한 것이며, 토큰 내부에는 위변조 방지를 위해 개인키를 통한 전자서명도 들어있다.
따라서 사용자가 JWT 를 서버로 전송하면 서버는 서명을 검증하는 과정을 거치게 되며 검증이 완료되면 요청한 응답을 돌려준다.

- JWT 구조
  ![image](https://user-images.githubusercontent.com/68368633/202860264-f46ad6a6-db7d-4526-b904-906f06cf1130.png)
  
  - Header
    - alg: 서명 암호화 알고리즘(ex: HMAC SHA256, RSA)
    - typ: 토큰 유형
  - Payload
    토큰에서 사용할 정보의 조각들인 Claim이 담겨있음
    *Claim: key-value 형식으로 이루어진 한 쌍의 정보
  - Signature
    시그니처에서 사용하는 알고리즘은 헤더에서 정의한 알고리즘 방식(alg)을 활용
    시그니처의 구조는 (헤더 + 페이로드)와 서버가 갖고 있는 유일한 key 값을 합친 것을 헤더에서 정의한 알고리즘으로 암호화

[참고링크1](https://inpa.tistory.com/entry/WEB-%F0%9F%93%9A-JWTjson-web-token-%EB%9E%80-%F0%9F%92%AF-%EC%A0%95%EB%A6%AC#JWT_(JSON_Web_Token))

[참고링크2](https://hudi.blog/self-made-jwt/)

### JWT 로그인 구현하기
1. Custom User Model 사용
  ```python
    # models.py
    class User(AbstractBaseUser):
        email = models.EmailField(max_length=30, unique=True)
        nickname = models.CharField(max_length=10)
        password = models.CharField(max_length=30)
        introduce = models.CharField(max_length=200)
        image = models.TextField(blank=True)
        is_public = models.BooleanField(default=False)
        search = models.BooleanField(default=False)
    
        is_active = models.BooleanField(default=True)
        is_superuser = models.BooleanField(default=False)
    
        objects = UserManager()
        USERNAME_FIELD = 'email'
    
        class Meta:
            db_table = "User"
    
        def __str__(self):
            return self.nickname
    
        @property
        def is_staff(self):
            return self.is_superuser
   ```
  Django의 기본 유저 모델에서 AbstractBaseUser를 상속받아 커스텀 모델로 변화시켰다. is_superuser로 관리자 여부를 확인하며 user, superuser를 생성하는 메소드는 UserManager에 추가하였다.

2. 회원가입 구현
   ```python
   # serializers.py
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
    ```
   ```python
   # views.py
   class JoinView(APIView):
    serializer_class = JoinSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "email": user.email,
                    "nickname": user.nickname,
                    "message": "가입이 성공적으로 이뤄졌습니다.",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   ```
   ![image](https://user-images.githubusercontent.com/68368633/202860281-ca0a1161-5c55-4535-b769-cd849fcc7ccc.png)
   ![image](https://user-images.githubusercontent.com/68368633/202860300-64191607-c20f-4c29-8c1f-a99cf0cec66f.png)

3. 로그인 구현
   ```python
   # serializers.py
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
   ```
   ```python
   # views.py
   class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            email = serializer.validated_data['email']
            access = serializer.validated_data['access']
            refresh = serializer.validated_data['refresh']
            # data = serializer.validated_data
            res = Response(
                {
                    "message": "로그인되었습니다.",
                    "email": email,
                    "access": access,
                    "refresh": refresh
                },
                status=status.HTTP_200_OK,
            )
            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   ```
   ![image](https://user-images.githubusercontent.com/68368633/202860313-d52e1d7f-848c-49ac-a059-ca61351253db.png)
   ![image](https://user-images.githubusercontent.com/68368633/202860319-68543091-09d9-4fd7-b108-8483482f79f2.png)
   ![image](https://user-images.githubusercontent.com/68368633/202860338-1cc96607-e09b-4999-a222-8ad88da323f5.png)


### 에러 해결
- Password Column 길이 에러

  ![image](https://user-images.githubusercontent.com/68368633/202860350-4083f5d9-5946-42da-92e2-2b9a1e000802.png)
  
  ALTER TABLE [TABLE명] modify [COLUMN명] VARCHAR(1000);
  
  mysql 명령어로 해당 필드 길이 늘려서 해결

### 회고
너무 어려웠다..😩 어느정도 하고 나서 뒤에 어렵지 않겠지하고 여유롭게 했는데 이리해도 저리해도 안돼서 몇번이나 다시하고 그랬다. 하하. 내가 혼자 느끼기에도 지금 내 코드가 상당히 비효율적이고 더러운 것 같아서 다음에 꼭 리펙토링을 하고 싶다.
그리고 저번에 viewset이나 url에서 router를 쓰는 작업을 하면서 코드가 간결해졌는데 이번 과제에서는 다시 APIView와 as_view()를 사용해서 두 가지 코드 형식이 같이 있는게 맞는지 모르겠다. 우선 보기에 깔끔하지는 않은 것 같다. 얼렁뚱땅 과제 끝 😎

----
## 6주차 미션 : Docker 배포 환경 구축
### 로컬 환경에서 도커 실행

<code>docker-compose -f docker-compose.yml up --build</code>

터미널에서 실행하여 브라우저에서 127.0.0.1:8000 접속 테스트

<사진>

접속 성공!

실행했을 때 모듈 임포트 에러가 많이 발생했는데 pip list로 requirements.txt에 추가가 필요한 내용들 찾아서 수정하여 해결하였다.

<code>docker-compose -f docker-compose.prod.yml down -v</code> 입력하여 종료

### 실 환경 배포
- AWS EC2 서버 구축: [참고링크](https://velog.io/@sanbonai06/AWS%EC%84%9C%EB%B2%84-%EA%B5%AC%EC%B6%95)
- AWS RDS 구축: [참고링크](https://velog.io/@sanbonai06/AWS-RDS-%EA%B5%AC%EC%B6%95)

#### .env.prod 생성
```
DATABASE_HOST={RDS db 주소}
DATABASE_DB=mysql
DATABASE_NAME={RDS 기본 database 이름}
DATABASE_USER={RDS User 이름}
DATABASE_PASSWORD={RDS master 비밀번호}
DATABASE_PORT=3306
DEBUG=False
DJANGO_ALLOWED_HOSTS={EC2 서버 ip 주소}
DJANGO_SECRET_KEY={django secret key}
```
프로젝트 상단에 파일 생성 후 내가 구축한 서버 내용 넣기! &rarr; 기존 .env 파일명을 바꾸고 해당 .env.prod를 .env로 바꿔서 위 내용이 연결되게 함

#### github secrets 설정
<사진>
- ENV_VARS: .env.prod 전체 복사 붙여넣기
- HOST: 배포할 EC2 서버 퍼블릭 DNS(IPv4) 주소
- KEY: 배포할 EC2 서버로 접근 가능한 ssh key 전문 (.pem)

#### push 후 Actions 확인
<사진>

<사진>

<code>deploy.yml</code>에 branch를 master로 설정했기 때문에 master branch에서 push했을 때 자동으로 배포된다.

### 테스트 API 확인
<사진>

postman에서 배포된 EC2 DNS 주소로 접속하여 api 확인

<사진>

데이터베이스에서 보면 잘 저장된 것을 확인할 수 있다.

### 회고
첫 배포를 끝냈다!! 내가 틀려도 뭘 틀렸는지 확인하기가 어려워서 지금까지 했던 과제 중에 안됐을 때 가장 막막하고 힘들었다.. 제가 모자라서.. 모자라서 그럽니다. 🧢
이런 나를 끝까지 도와주신 민준님께 감사의 말씀 올립니다 그저 빛!
