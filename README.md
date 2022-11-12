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
