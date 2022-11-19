# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포


## 2주차 미션: DB 모델링 및 Django ORM

### 투두메이트
일정 관리(투두리스트) 서비스.  
다른 사용자들에게 자신의 투두리스트를 공유할 수 있다는 차별점이 있다.  
서로 좋아요 등을 남길 수도 있고, 그래서 더 동기부여가 된다!

### 모델 설계

#### User
django에서 기본 제공하는 user 모델 상속  - AbstractUser를 상속받아 custom함
- email을 유저네임으로 사용하도록 custom

#### Follower
- follower: User를 참조하는 foreign key
- following: User를 참조하는 foreign key

#### Category
- category_name: 카테고리명
- user : User를 참조하는 foreign key, 어떤 사용자의 카테고리인지 보여줌

#### Todo
- todo_name: to do item을 작성했을 때 그것의 이름
- user: 작성한 사용자
- category: 카테고리
- disclosure_choice: 친구들에게 공개할 것인지 여부, private(비공개), only friends(친구 공개), public(전체 공개) 중 선택할 수 있도록 한다.  
default는 public(전체공개)
- date: 일정별 to do list를 볼 수 있도록

#### Comment
- todo: Todo를 참조하는 foreign key, 어떤 to do item에 대한 활동인지 보여줌
- author: User를 참조하는 foreign key, 이모티콘이나 댓글을 다는 작성자
- emoji: 한 글자짜리 이모티콘으로 반응
- comment: 서로 댓글을 달 수도 있다.

### ORM 이용해보기
1번  
![img](https://user-images.githubusercontent.com/86969518/194710346-239846d9-ff7a-4101-b47d-d40bc5b2a6e7.png)  
2번  
![img_1](https://user-images.githubusercontent.com/86969518/194710347-05da1fba-e2de-4d77-89c3-4c9775e5f404.png)  
3번  
![img_2](https://user-images.githubusercontent.com/86969518/194710348-60bedf6a-3168-4566-80d0-c4bb2588e6aa.png)  


### 이번 과제를 하며...
내 컴퓨터 환경에서는 pip install mysqlclient로 mysqlclient가 설치되지 않는다..  
그래서 지난번 프로젝트 때는 파이썬 버젼에 맞는 whl 파일을 인터넷에서 다운로드 받는 형식으로 이용을 했는데
다른 방법이 없나 알아봤지만 결국 이번에도 수동설치를 하게 되었다.  

또, mysql 데이터베이스를 그대로 이용할 수 없다.  
python manage.py migrate를 하면 다음 에러가 뜬다.  
![img_3](https://user-images.githubusercontent.com/86969518/194710349-3090c3dd-dae1-4c0e-bb7b-3675343417d1.png)
이 에러를 해결하려고 시간을 엄청나게 많이 썼는데..! 답은 pip install PyMySQL을 하는 것이었다.  
다음에는 잊지 말아야지..

드디어 데이터베이스를 연결하고 모델링을 하는데, 생각보다 복잡했다!  
투두메이트는 들어보기만 하고 사용해본 적은 없는데, 그냥 투두리스트가 아니라
사용자 간 소통하는 기능이 있어서 생각할 것이 많았다. 사실 실제 앱처럼 하려면 이것보다 훨씬
복잡하고 꼼꼼하게 해야할 것 같은데, 이번 과제에서 그렇게까지 하지는 못해서 아쉽다.  

그리고 Django에서 기본적으로 제공하는 user 모델에 대해서 잘 몰랐는데, 엄청 편리한 기능 같아서
더 알아보고 싶다.


## 3주차 미션: Django Serializer & Django View

### 데이터 삽입

User 데이터 삽입
```python
class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
```
![img_4](https://user-images.githubusercontent.com/86969518/194710350-f3221c17-77b9-48f9-8fae-b0a8851ce411.png)

Category 데이터 삽입
```python
class Category(models.Model):
    category_name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.category_name
```
![img_5](https://user-images.githubusercontent.com/86969518/194710352-3eba33fa-06fc-4c9f-bd6c-9698975b96fa.png)

Todo 데이터 삽입
```python
class Todo(models.Model):
    DISCLOSURE_CHOICES = {
        ('private', 'Private'),
        ('onlyFriends', 'Only Friends'),
        ('public', 'Public'),
    }
    todo_name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    disclosure_choice = models.CharField(default='public', max_length=30, choices=DISCLOSURE_CHOICES)
    date = models.DateTimeField(default=now)
    def __str__(self):
        return self.todo_name
```
![img_6](https://user-images.githubusercontent.com/86969518/194710353-f8e9d88d-6c31-47e1-98c5-600ec1e5a9c3.png)

### API 만들기
모든 데이터를 가져오는 api
![img_7](https://user-images.githubusercontent.com/86969518/194710354-bc8bfc8c-48b2-4a71-b9b2-39ea3b91f971.png)

특정 과제를 가져오는 api
![img_8](https://user-images.githubusercontent.com/86969518/194710355-cace0bfb-55ab-4586-83d0-77456f36958a.png)

새로운 데이터를 create하도록 요청하는 api
![img_9](https://user-images.githubusercontent.com/86969518/194710357-454fea29-7679-4404-b5e8-06ca453d4e4e.png)

특정 데이터를 삭제하는 api
![img_10](https://user-images.githubusercontent.com/86969518/194710323-09048a9e-78f4-4416-9338-341a1bef1d74.png)
![img_11](https://user-images.githubusercontent.com/86969518/194710301-62ec507c-7ed0-4b05-8224-458d7e51551b.png)

특정 데이터를 업데이트하는 api
![img_12](https://user-images.githubusercontent.com/86969518/194710255-74b188f5-0d7e-4d02-8849-ed2c8fc5f375.png)
![img_13](https://user-images.githubusercontent.com/86969518/194710183-c6f6fcf8-a487-45a5-90d7-8d40a661612d.png)


### 이번 과제를 하며...
모델들에 대해 ModelSerializer을 이용해 serializer를 만들었고,
가장 핵심 모델이라고 생각한 todo 모델에 대해 view 만들기 연습을 해봤다.

views.py를 작성할 때 처음에 과제 예시로 나온 코드를 그대로 따라했더니 오류가 났는데 해결 과정에서
JsonResponse 대신 그냥 Response를 사용해야 drf를 테스트 할 수 있는 브라우저 화면을 볼 수 있다는 사실을 알게 되었고,  
함수형 뷰를 작성할 때는 @api_view를 꼭 달아야한다는 사실도 알게 되었다.

나중에 서비스에 필요한 나머지 api들도 만들고 Postman도 한번 사용해 봐야겠다!

## 4주차 미션: DRF2 - API View & Viewset & Filter

### Model 수정
```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```
BaseModel을 정의하고 Category, Todo, Comment Model이 BaseModel을 상속받아 created_at과 updated_at 속성을 갖게 했다.
  
```python
is_completed = models.BooleanField(default=False)
```
Todo가 완료되었는지 체크하는 기능이 빠진 것 같아서 Todo에 is_completed attribute을 추가했다.

### 기존 FBV로 작성했던 API
저번주 과제에서 수정된 부분: 잘못 사용된 status number 수정, url 고치기(todo/ 에서 todos/로)  
* get_object_or_404는 사용해보려고 했으나
```python
todo = get_object_or_404(Todo,id=pk)
```
를 적었을 때 'Todo' object is not iterable 에러가 발생했고 시간이 없어서 해결은 못하고 결국 원래 사용했던 방식으로 돌아갔다. 다음에 다시 시도해볼 예정이다.
```python
#Function-Based View - views.py
@csrf_exempt
@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todo_items = Todo.objects.all()
        serializer = TodoSerializer(todo_items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def todo_item(request, pk):
    if request.method == 'GET':
        todo = Todo.objects.filter(id=pk)
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        todo_instance = Todo.objects.get(id=pk)
        serializer = TodoSerializer(instance=todo_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        todo = Todo.objects.filter(id=pk)
        todo.delete()
        return Response(status=204)
```
```python
#Urls for Fuction-Based View
urlpatterns = [
    #Todo
    path('todos/', views.todo_list, name="todo_list"),
    path('todo/<int:pk>', views.todo_item, name="todo_item"),
]
```
### DRF API View의 CBV으로 리팩토링하기
```python
#Class-Based View - views.py
class TodoList(APIView):
    def get(self, request, format=None):
        todo_items = Todo.objects.all()
        serializer = TodoSerializer(todo_items, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
class TodoItem(APIView):
    def get(self, request, pk, format=None):
        todo = Todo.objects.filter(id=pk)
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        todo_instance = Todo.objects.get(id=pk)
        serializer = TodoSerializer(instance=todo_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    def delete(self, request, pk, format=None):
        todo = Todo.objects.filter(id=pk)
        todo.delete()
        return Response(status=204)
```
```python
urlpatterns = [
    #Todo
    path('todos/', TodoList.as_view(), name="todo-list"),
    path('todo/<int:pk>/', TodoItem.as_view(), name="todo-item"),
]
```

### Viewset으로 리팩토링하기 & filter 기능 구현하기
구현한 filter 기능:
1. user filtering
2. disclosure_choice(public, only friends, private)에 따른 filtering
3. recent_todos (method 사용해 custom filtering): date(todo를 설정한 날짜)가 7일 이내인 todo만 보여주기

```python
#Viewset - views.py
class TodoFilter(FilterSet):
    user = filters.ModelChoiceFilter(queryset=User.objects.all())
    disclosure_choice = filters.TypedChoiceFilter(choices=Todo.DISCLOSURE_CHOICES)
    recent_todos = filters.BooleanFilter(method='filter_recent_todos', label='recent_todos')
    class Meta:
        model = Todo
        fields = ['user', 'disclosure_choice']

    def filter_recent_todos(self, queryset, name, value):
        queryset = Todo.objects.all()
        filtered_queryset = queryset.filter(date__gte=datetime.now()-timedelta(days=7))
        filtered_queryset_false = queryset.exclude(pk__in=filtered_queryset)

        if(value==True):
            return filtered_queryset
        else:
            return filtered_queryset_false


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter
```
```python
#Viewset - urls.py
router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = router.urls
```

### 이번 과제를 하며...
같은 API를 다양하게 만들어보며 api 만들기에 대한 이해도가 높아진 것 같다. Viewset은 이번 과제를 하며 처음 알게 된 방식인데 너무 편리해서 깜짝 놀랐다.  
이렇게 적게 썼는데 기능이 다 완성됐다고?  

그리고 filterset도 처음 사용해봤는데 앞으로 유용하게 사용할 것 같다. 과제를 하면서 찾아봤는데 아주 다양한 종류가 있었다.  

오늘도 또 django가 편리한 프레임워크임을 느꼈다. 또 custom을 해서 사용하는 법도 잘 알아야겠다는 생각을 했다.

## 5주차 미션: DRF3 - Simple JWT

### Q1. 로그인 인증 방식은 어떤 종류가 있나요?
1. <b>세션과 쿠키를 이용한 인증</b>  
브라우저에 존재하는 쿠키에 세션 id를 발급하고 매 요청마다 브라우저의 쿠키를 검증하여 세션 아이디를 통해 사용자를 인증한다.
2. <b>Access Token을 이용한 인증</b>  
JWT 이용 (인증에 필요한 정보 암호화한 토큰)
3. <b>Access Token + Refresh Token을 이용한 인증</b>  
Access token의 유효기간이 짧으면 사용자가 로그인을 자주 해야 돼서 번거롭고, 유효기간이 길면 보안에 취약하다는 단점이 있다.  
이를 해결하기 위한 것이 Refresh token.
4. OAuth 2.0을 이용한 인증
5. SNS 로그인

### Q2. JWT는 무엇인가요?
JWT는 Json Web Token의 약자이다.
dot(.)을 구분자로 3파트로 구분되어 있으며 각각의 파트를 Header, Payload, Signature라 부르며 각각 필요한 정보들을 담아 보관한다.

토큰 자체에 인증에 필요한 정보가 모두 있기에 별도의 인증 저장소가 필요 없고,
별도의 사용자 정보를 요청할 필요가 없기에 데이터 요청이 좀 더 가벼워 질 수 있다는 장점이 있다.


### Q3. JWT 로그인 구현하기

#### User model refactoring
User model을 너무 간단하게 만들었던 것 같아서 리팩토링을 진행했다 (지금도 간단하긴 하다,,) 

기존에는 email과 password 필드만 있었는데, id와 nickname 필드를 추가했다.
그리고 지난 주에 todo, category, comment 모델이 상속받게 한 BaseModel을 user 모델도 상속받게 하며 
deleted_at도 추가해 soft delete를 가능하게 했다.  
(soft delete는 User model에만 사용하려고 하는데 User model에 대한 views는 아직 작성하지 않았다.)


```python
# models.py
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now
        self.save(update_fields=['deleted_at'])

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, id, nickname, email, password, **extra_fields):
        if not id:
            raise ValueError('Users require an id field')
        if not nickname:
            raise ValueError('Users require a nickname field')
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(id=id, nickname=nickname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, id, nickname, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(id, nickname, email, password, **extra_fields)

    def create_superuser(self, id, nickname, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(id, nickname, email, password, **extra_fields)


class User(AbstractBaseUser, BaseModel):
    id = models.CharField(max_length=20, primary_key=True)
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'nickname', ]

    def __str__(self):
        return self.nickname
```

#### 회원가입 구현
![image](https://user-images.githubusercontent.com/86969518/202844844-223ca836-9574-4b2b-bebe-68cab5bdf25c.png)
![image](https://user-images.githubusercontent.com/86969518/202844872-9d003c9d-f69e-4aff-99da-ecc4bbcb5267.png)
```python
#serializers.py
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        id = validated_data.get('id')
        nickname = validated_data.get('id')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            id=id,
            nickname=nickname,
            email=email,
            password=password
        )
        user.set_password(password)
        user.save()
        return user
    
    
#views.py
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
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
#### 로그인 구현
로그인 성공
![image](https://user-images.githubusercontent.com/86969518/202844929-42cc447e-69eb-4095-b011-9038321444a2.png)
![image](https://user-images.githubusercontent.com/86969518/202844960-1e438583-f992-4a1c-bddf-c6479e1619f5.png)

로그인 실패
![image](https://user-images.githubusercontent.com/86969518/202845054-0548f8c7-5bdd-4191-a134-3e492e5d7956.png)
![image](https://user-images.githubusercontent.com/86969518/202845083-76b473da-937b-4537-bee4-14774ec1b729.png)

```python
#serializers.py
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


#views.py
class AuthView(APIView):

    def post(self, request):
        user = authenticate(
            id=request.data.get("id"), password=request.data.get("password")
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response({"no such user"}, status=status.HTTP_400_BAD_REQUEST)
```
Token Refresh  
<b>from rest_framework_simplejwt.views import TokenRefreshView</b>를 이용해 token refresh를 구현했다.  
아직 사용법을 제대로 찾아보지는 못해서 어떻게 동작하는 건지는 나중에 자세히 조사해 볼 예정..

```python
#api/urls.py
urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterAPIView.as_view()),
    path("auth/", AuthView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
]
```
### 이번 과제를 하며..
단순한 기능 구현을 넘어서 보안까지 생각해볼 수 있어서 좋았던 과제였다. 나중에 Logout 기능도 구현해야겠다.