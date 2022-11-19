# CEOS 16기 백엔드 스터디

## 5주차 미션 : Simple JWT

### Abstract User

  <pre><code>
  # models.py
  
  class User(BaseModel, AbstractUser):
      email = models.EmailField(max_length=250, unique=True)
      password = models.CharField(max_length=150)
  
      def __str__(self):
          return self.username
  
  </code></pre>
  
  처음에 email과 password 컬럼 길이를 작게 설정했더니 password가 암호화되는 과정에서 길이가 길어지면서 
  <code>django.db.utils.DataError: (1406, "Data too long for column 'password' at row 1")</code> 에러가 발생하여
  길이를 더 크게 지정해주었다.

### Simple JWT를 이용한 로그인 구현

  <pre><code>
  # serializers.py

  class UserSerializer(serializers.ModelSerializer):
  
      todo_list = TodoSerializer(many=True, read_only=True)
  
      class Meta:
          model = User
          fields = '__all__'



  # views.py
  
  class LoginView(APIView):
      def post(self, request):
          user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
  
          if user is not None:
              serializer = UserSerializer(user)
              token = TokenObtainPairSerializer.get_token(user)
              refresh_token = str(token)
              access_token = str(token.access_token)
              res = Response(
                  {
                      "message": "login success",
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
          else:
              return Response({"message": "login fail"}, status=status.HTTP_400_BAD_REQUEST)
  
  </code></pre>

  Viewset으로 구현하고 싶었지만 많은 레퍼런스들이 CBV로 나와있어서 CBV 형태로 구현하였다. rest_framework_simplejwt에서 제공하는
  <code>TokenObtainPairSerializer</code>를 사용하여 토큰을 발급하였다. 
  
  
  - <code>authenticate(request=None, **credentials)</code> : username과 password를 받아서 모든 authentication backend에 검사하여
  credential이 유효하다면 유저 객체를 반환하고 그렇지 않다면 None을 반환

  검증을 위하여 <code>python manage.py createsuperuser</code> 명령어를 사용하여 admin 유저들을 생성하였다. 

  ![createsuperuser](https://user-images.githubusercontent.com/74910760/202854531-326a3249-d01c-43ca-a3c9-c874cfd400e5.png)

  로그인 기능이 제대로 구현되었는지 확인하기 위해 postman을 사용하여 검증해보았다. 
  
  <img width="1011" alt="성공시" src="https://user-images.githubusercontent.com/74910760/202854687-7e73a36a-139d-4dc9-a4bf-7ceec6236283.png">
  
  accessToken과 refreshToken이 성공적으로 잘 나오는 것을 확인할 수 있다.

  <img width="1009" alt="실패시" src="https://user-images.githubusercontent.com/74910760/202854761-aebe73fb-be9c-489e-8eea-46b4cf2665ca.png">

  유저 이름이나 비밀번호가 틀렸을 때는 "login fail"이 뜨며 검증이 잘 된다.

  

### 회고
기존의 user모델에서 AbstractUser로 커스텀한 유저를 사용하고 나니 여러 개의 컬럼이 <code>not null</code> 처리가 되어 기존의 쿼리를 통한 사용자 추가가 어려워졌다. 그래서 
createsuperuser를 통해 admin 사용자를 추가하여 사용하였다. 이번 과제에서는 너무 다양한 레퍼런스가 있어 오히려 어떠한 방식으로 구현해야할 지 고르는 것이 매우 어려웠다. 그리고 어느 과제보다도
많은 에러가 생겨서 더 어렵게 느껴졌다. 

토큰을 생성하는 과정에서 처음에는 <code>TokenObtainSerializer</code>를 사용했는데 계속 for_user 라는 문구로 에러가 떴다. 해당 Serializer를 
까보니 리턴 값에 <code>for_user()</code>라는 함수가 사용되었다. <code>TokenObtainPairSerializer</code>를 사용하니 그냥 data만을 리턴해주고 해당 에러가 뜨지 않았다. 
에러가 나오지 않아서 사용하긴 했는데 아직 왜 에러가 생긴건지는 잘 모르겠다. 그 부분에 대해서는 앞으로 더 공부를 해볼 예정이다.



## 4주차 미션 : API View & Viewset & Filter

### API View를 이용한 CBV 구현


  <pre><code>
  # views.py
  
  class TodoListsAPI(APIView):
    def get(self, request):
        items = TodoSerializer(Todo.objects.all(), many=True)
        return Response(items.data)

    def post(self, request):
        req_data = JSONParser().parse(request)
        result = TodoSerializer.create(TodoSerializer, req_data)
        return Response(result)


  class TodoListAPI(APIView):
      def get(self, request, pk):
          item = TodoSerializer(Todo.objects.get(id=pk))
          return Response(item.data)
  
      def delete(self, request, pk):
          result = TodoSerializer.delete(TodoSerializer, pk)
          return Response(result)
  
      def put(self, request, pk):
          req_data = JSONParser().parse(request)
          result = TodoSerializer.update(TodoSerializer, pk, req_data)
          return Response(result)
  </code></pre>

### ViewSet으로 리팩토링

- ViewSet 구현
    <pre><code>
    # views.py
  
    class TodoListViewSet(viewsets.ModelViewSet):
        serializer_class = TodoSerializer
        queryset = Todo.objects.all()
    </code></pre>


- router
    <pre><code>
    # urls.py
  
    router = routers.DefaultRouter()
    router.register(r'todos', TodoListViewSet, basename='todo')

    urlpatterns = router.urls
    </code></pre>

  <code>router.register</code>를 통해 라우터에 Viewset을 등록하여 urlconf가 
자동으로 생성되도록 한다. 

#### ModelViewSet 클래스에서 제공하는 작업
- <code>list()</code> : method GET
- <code>retrieve()</code> : method GET, 특정 pk
- <code>create()</code> : method POST
- <code>update()</code> : method PUT
- <code>partial_update()</code> : method PATCH
- <code>destroy()</code> : method DELETE



### filter 기능 구현

url의 쿼리를 통해 원하는 결과값을 얻을 수 있다.
- FilterSet
    <pre><code>
    # views.py
  
    class TodoListFilter(FilterSet):
        contents = filters.CharFilter(field_name='contents', lookup_expr='icontains')
        is_done = filters.BooleanFilter(method='filter_is_done')
    
        class Meta:
            model = Todo
            fields = ['contents', 'is_checked']
    
        def filter_is_done(self, queryset, name, value):
            return queryset.filter(type=value)
    </code></pre>

  - contents의 내용을 value값에 입력된 값으로 해당되는 값을 필터링해주었다. <code>icontains</code>를 사용하여 
쿼리 입력 값이 포함된 모든 contents를 포함한 객체들이 반환된다.

  - is_checked 컬럼을 필터링해주기 위해 custom 필터링 메소드를 정의해주었다. value에 값에 해당되는 결과를 반환해준다. 

  
- ViewSet

    <pre><code>
    # views.py
  
    class TodoListViewSet(viewsets.ModelViewSet):
        serializer_class = TodoSerializer
        queryset = Todo.objects.all()
        filter_backends = [DjangoFilterBackend]
        filterset_class = TodoListFilter
    </code></pre>

    - <code>DjangoFilterBackend</code>는 설정 파일에서 전역적으로 설정해주거나, 개별 View나 ViewSet에 설정해주면 된다. 

### 회고 및 수정사항

1. restful API를 만족하도록 <code>todo -> todos</code>로 변경
2. ViewSet로 create 실행 시 read_only로 지정해둔 user를 참조하면서 오류 발생. serializer에서 read_only 삭제

ViewSet을 사용했을 때 내가 생각한 것보다 더 대부분의 것을 장고에서 자동으로 처리해줘서 이게 어떻게 제대로 돌아가는 것인지 
궁금했다. ViewSet으로 변경하는 과정에서 이전에 만들어둔 응답 컨벤션을 사용하지 못하게 되었는데 ViewSet의 Permission을 이용하여 
다시 생성할 수 있다는 걸 늦게 알아 구현하지 못했다,,, 이후에 구현해볼 예정이다. 점점 더 구조화된 API를 설계하며 발전해가는 것 같아 뿌듯하다. 

***

## 3주차 미션 : Serializer, API 구현

- Todo 모델
    <pre><code>
    # models.py

    class Todo(BaseModel):
        user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='todo')
        contents = models.TextField(max_length=30)
        date = models.DateField()
        is_checked = models.BooleanField(default=False)
    </code></pre>
### 데이터 삽입

- Todo 모델 데이터

    ![Todo objects](https://user-images.githubusercontent.com/74910760/194697856-ce2c7c13-8e30-4ce4-b90e-1f242ffd99c7.png)

### API 구현

#### 모든 데이터를 가져오는 API
- URL : <code> http://127.0.0.1:8000/api/todo/ </code>
- method : <code> GET </code>
- Response
  <pre>
  <code>[
        {
            "id": 1,
            "created_at": "2022-10-06T18:33:42.923509+09:00",
            "updated_at": "2022-10-06T18:33:42.923688+09:00",
            "contents": "swimming",
            "date": "2022-10-04",
            "is_checked": false,
            "user": 1
        },
        {
            "id": 2,
            "created_at": "2022-10-06T18:34:11.865900+09:00",
            "updated_at": "2022-10-06T18:34:11.866042+09:00",
            "contents": "dancing",
            "date": "2022-09-30",
            "is_checked": true,
            "user": 2
        },
        {
            "id": 3,
            "created_at": "2022-10-06T18:34:38.723939+09:00",
            "updated_at": "2022-10-06T18:34:38.724032+09:00",
            "contents": "programming",
            "date": "2022-09-30",
            "is_checked": true,
            "user": 3
        },
        {
            "id": 5,
            "created_at": "2022-10-06T18:37:19.544185+09:00",
            "updated_at": "2022-10-06T18:37:19.547595+09:00",
            "contents": "playing games",
            "date": "2022-10-01",
            "is_checked": false,
            "user": 3
        },
        {
            "id": 6,
            "created_at": "2022-10-06T18:37:48.989935+09:00",
            "updated_at": "2022-10-06T18:37:48.990048+09:00",
            "contents": "biking",
            "date": "2022-09-10",
            "is_checked": false,
            "user": 1
        }
    ]</code>
  </pre>

#### 특정 데이터를 가져오는 API
- URL : <code> http://127.0.0.1:8000/api/todo/<ink:pk>/ </code>
- method : <code> GET </code>
- request id : 3
- Response
  <pre>
    <code>{
        "id": 3,
        "created_at": "2022-10-06T18:34:38.723939+09:00",
        "updated_at": "2022-10-06T18:34:38.724032+09:00",
        "contents": "programming",
        "date": "2022-09-30",
        "is_checked": true,
        "user": 3
    }</code>
  </pre>

#### 새로운 데이터를 create하도록 요청하는 API
- URL : <code> http://127.0.0.1:8000/api/todo/ </code>
- method : <code> POST </code>
- Body 데이터 (JSON)
  <pre>
  <code>{
      "user_id" : 3,
      "contents" : "drinking",
      "date" : "2022-10-13"
  }
  </code></pre>
- Response
  - 성공 시
    <pre>
    <code>{
        "message": "할 일을 생성하였습니다.",
        "data": {
            "id": 66,
            "created_at": "2022-10-08T17:25:44.012639+09:00",
            "updated_at": "2022-10-08T17:25:44.044957+09:00",
            "contents": "drinking",
            "date": "2022-10-13",
            "is_checked": false,
            "user": 3
        }
    }</code>
    </pre>
  - 실패 시 (요청 id의 유저가 존재하지 않을 때)
    <pre>
    <code>{
        "message": "해당 유저를 찾을 수 없습니다."
    }
    </code></pre>

#### 특정 데이터를 삭제하는 API
- URL : <code> http://127.0.0.1:8000/api/todo/<int:pk>/ </code>
- method : <code> DELETE </code>
- Response
  - 성공 시
    <pre>
    <code>{
        "message": "삭제 성공"
    }
    </code></pre>
  - 실패 시 (요청 id의 todo가 존재하지 않을 때)
    <pre>
    <code>{
        "message": "해당 기록을 찾을 수 없습니다."
    }
    </code></pre>

#### 특정 데이터를 업데이트하는 API
- URL : <code> http://127.0.0.1:8000/api/todo/<int:pk>/ </code>
- method : <code> PUT </code>
- request id : 5
- Body 데이터 (JSON)
  <pre>
  <code>{
    "contents" : "math test",
    "date" : "2022-09-18",
    "is_checked" : true
  }
  </code></pre>
- Response
  - 성공 시
    - 기존 데이터
      <pre>
      <code>{
          "id": 5,
          "created_at": "2022-10-06T18:37:19.544185+09:00",
          "updated_at": "2022-10-06T18:37:19.547595+09:00",
          "contents": "playing games",
          "date": "2022-10-01",
          "is_checked": false,
          "user": 3
      }
      </code></pre>
    - 업데이트 후
      <pre>
      <code>{
          "message": "업데이트 완료",
          "data": {
              "id": 5,
              "created_at": "2022-10-06T18:37:19.544185+09:00",
              "updated_at": "2022-10-08T17:35:54.167008+09:00",
              "contents": "math test",
              "date": "2022-09-18",
              "is_checked": true,
              "user": 3
          }
      }
      </code></pre>
  - 실패 시 (요청 id의 todo가 존재하지 않을 때)
    <pre>
    <code>{
        "message": "해당 기록을 찾을 수 없습니다."
    }
    </code></pre>

### 회고

1. 마이그레이션 실수로 디비를 통채로 날렸다... 덕분에 마이그레이션 동작 방식을 정확히 알게되었다,,하하 앞으로는 마이그레이션 파일 멋대로 지우지 말기,,
2. get으로 데이터를 찾을 때 해당하는 데이터가 없다면 <code> DoesNotExist </code> 에러가 뜬다. 
   에러를 사용하여 성공 시, 실패 시 다른 리턴 메세지를 주었다. 다음에는 status code도 추가해줄 예정이다.
3. delete()를 한 후 save()를 사용해주었더니 해당 데이터가 삭제되고 바로 재생성되는 요상한 에러를 발견할 수 있었다. 
   새로운 데이터가 생성되거나 기존 데이터가 업데이트될 때만 save()를 사용해주자.
4. 장고로 API를 구현해보지는 않았지만 다른 프레임워크로 API 구현하는 것과 매우 유사해서 저번주 과제보다는 쉬운 편이었다. 장고를 더 이해해서 
   리팩토링도 해봐야곘다..
5. 더 완벽한 에러처리를 위해 exception_handler와 logger를 사용하다가 기존에 구현한 API가 이상하게 작동해버려서 결국 다 지워버렸다,, 다음기회에 발전시켜보기로 하자.
***
  
## 2주차 미션: DB 모델링 및 Django ORM

#### Todo Mate 기능
- 날짜별 할 일 추가 및 관리
- 이모지, 사진을 이용한 오늘 하루 일기 작성
- 서로 팔로우하며 친구의 일정, 일기에 좋아요 응원 


### erd

#### User
![User](https://user-images.githubusercontent.com/74910760/193414501-044002c3-4abc-4da4-aa6a-5f7f59e688b1.png)
#### Todo
![Todo](https://user-images.githubusercontent.com/74910760/193414524-afbb6f57-4f86-4cbc-a76f-afe0c0d02fcc.png)
- user와 1:N 관계 : foriegn key로 user 지정
- date 입력 형식 지정
#### Diary
![Diary](https://user-images.githubusercontent.com/74910760/193414540-bbfbe2fa-ae8f-48b6-81ac-a8f83c99249a.png)
- user와 1:N 관계 : foriegn key로 user 지정
- date 입력 형식 지정
- 비공개 여부 private BooleanField 사용
#### Likes
![Likes](https://user-images.githubusercontent.com/74910760/193414559-0642a788-c633-4203-a10b-0bab85abe2c3.png)
- 유저(User)-좋아요 1:N 관계 : foriegn key로 유저 지정
- 유저 - 좋아요 - 할 일 N:M 관계 -> ManyToMany
- 유저 - 좋아요 - 일기 N:M 관계 -> ManyToMany
#### Follows
![Follows](https://user-images.githubusercontent.com/74910760/193414580-ae5e4f24-7be3-4e64-a9b3-eb73649251a1.png)
- 맞팔로우 서로 N:M 관계 -> ManyToMany


### ORM

- ForiegnKey 필드를 포함하는 Todo 모델 객체 생성
![ForiegnKey로 사용될 User 객체 생성](https://user-images.githubusercontent.com/74910760/193414608-ef404fdf-b704-4054-ab12-c71985dadf62.png)
![Todo 모델 객체 생성](https://user-images.githubusercontent.com/74910760/193414621-0024336c-e46a-4c0b-9d91-5c755b00efdd.png)
![Todo table](https://user-images.githubusercontent.com/74910760/193414636-7687baa7-48a3-4447-9b1d-70bed8a7667a.png)
- ORM 쿼리셋 조회
![Query](https://user-images.githubusercontent.com/74910760/193414652-dc645b55-795b-4176-9768-3ad51047411b.png)
- filter 사용
![filter](https://user-images.githubusercontent.com/74910760/193414662-d57c519c-dc48-4916-98ea-12ef935a1a0c.png)


### 회고

mysql 사용부터 migration을 하는 과정에서 에러가 많이 떠서 해결하는데 고생을 했다... 과제도 이전보다 난이도가 많이 높아져서 어려웠지만 1대다 관계, 다대다 관계등을 고민해보고 erd를 짜면서 각각 모델이 어떻게 연결되는지 이해할 수 있었다. 기억나는 에러사항은 
1. m1 환경에서는 settings.py에 pymysql을 다운받고 import하여 pymysql.install_as_MySQLdb()를 작성해주어야한다.
2. 원하는 날짜를 객체의 field값으로 넣어주고 싶을 때 input_format으로 형식으로 지정해줄 수 있다.

그리고 알게된 점은 

- CharField를 사용하고자 할 때는 max_length 값을 필수로 지정해준다.
- timezone으로 정확한 날짜와 시간을 사용하고자 한다면 setting에서 TIME_ZONE을 서울로 설정해준다.
- 원하는 형태로 객체를 확인하려면 def __str__(self)에서 리턴값을 설정해준다.

등이 있었다. erd를 완성하고 나서 실제 서비스를 구현하려면 더 세분화해서 모델을 작성했어야겠다는 생각이 들었다. 다음 스터디에서 피드백을 통해 erd를 더 발전시킬 수 있길...


