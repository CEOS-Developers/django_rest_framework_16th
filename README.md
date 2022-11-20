# CEOS 16기 백엔드 스터디 : TODO_MATE

### 5주차 미션 : 5주차 : DRF3 - Simple JWT
JWT가 궁금해서 구글링하다가 django에서 제공하는 jwt 로직을 찾아내서 해당 부분을 사용해 봤습니다.

#### - url 정의

    urlpatterns = [
        ~
        path('auth/', include('dj_rest_auth.urls')),
        path('auth/registration/', include('dj_rest_auth.registration.urls')),
    ]    

> 위에 한줄만 추가하면 아래의 url로 실행가능

* http://localhost:8000/api/auth/password/reset/
* http://localhost:8000/api/auth/password/reset/confirm/
* http://localhost:8000/api/auth/login/
* http://localhost:8000/api/auth/logout/
* http://localhost:8000/api/auth/user/
* http://localhost:8000/api/auth/password/change/
* http://localhost:8000/api/auth/token/verify/
* http://localhost:8000/api/auth/token/refresh/

#### - base 추가 변수
dj-rest-auth

    REST_USE_JWT # JWT 사용 여부, 요청값에 상세히 나오게끔!
    JWT_AUTH_COOKIE # 호출할 Cookie Key값
    JWT_AUTH_REFRESH_COOKIE# Refresh Token Cookie Key 값 (사용하는 경우)

django-allauth

    SITE_ID # 해당 도메인의 id
    ACCOUNT_EMAIL_REQUIRED # User email 필수 여부
    ACCOUNT_EMAIL_VERIFICATION# Email 인증 필수 여부


#### - jwt user custom

    # customize model
    USERNAME_FIELD = 'username' #'email'이라고 해주면 로그인 할때 email 써야함
    REQUIRED_FIELDS = []

    objects = UserManager()

> models.py -> user 

    class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Name must be set')
        # email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

> managers.py

#### - accessToken , refreshToken 정의
accessToken = 말 그대로 접근 가능 하게 해주는 Token
refreshToken = accessToken 이 만료 되었을 때 accessToken 을 갱신시켜주는 Token

#### - Authentication, Authorization(Permission) 정의
Authentication(인증) = user 가 누구인지 확인
Authorization(인가) = 차등적인 권한(ex. 관리자, 사용자)을 부여할 수 있음

*****
### 4주차 미션 : DRF2 - API View & Viewset & Filter
저번 주차에 Viewset을 사용하여 설계하였으므로 filter관련해서 정리하겠습니다.

filtering은 어떤 query set에 대하여 <b>원하는 옵션대로 필터</b>를 걸어, 특정 쿼리셋을 만들어내는 작업이라고 한다.

이번 주차에서 2가지의 방식을 사용함
1. filterset_fields - django-filter 
2. OrderingFilter - drf의 기본 필터

#### - filterset_fields
filterset_fields 를 지정해주면 equals로 비교하여 특정 쿼리셋의 결과 값을 반환해준다.

     filter_backends = (DjangoFilterBackend, OrderingFilter)
     filterset_fields = ['name', 'user', 'privacy']

하지만 자세한 비교는 불가능하여 보통 custom filterset도 많이 사용한다.

<img width="697" alt="스크린샷 2022-11-12 오후 5 40 13" src="https://user-images.githubusercontent.com/62806067/201466292-43882317-bbf0-4227-842e-cda255fdee79.png">

> content=project 쿼리 날려줌 , 부분일치와 같은 세부적인 부분은 고려 불가능

#### - OrderingFilter
OrderingFilter 에서 해당 필드를 정해주면 get에 ordering=date 이런식으로 명시해주면
date 오름차순으로 출력하여 준다.

     filter_backends = (DjangoFilterBackend, OrderingFilter)
     ordering_fields = ['date', 'like_count']
     ordering = ['date'] # default

<img width="696" alt="스크린샷 2022-11-12 오후 5 39 01" src="https://user-images.githubusercontent.com/62806067/201466255-27bf2eef-48d6-4858-bfac-d0bb826c2796.png">

> date 내림차순 정렬

#### - 총평
왜 custom filterset이 적용이 안되는지 아직 찾아내지 못했다.
그래서 아쉽긴하지만 fields로 구현해보았다.
이번에 확실히 api에 어떻게 날려야 원하는 값이 도출되는지 알게 된 것 같다.
pagination과 같은 기능들도 많던데 일단 안되는 이유 찾느라 여기 까진 고려하지 못했다.
OrderingFilter과 같이 SearchFilter도 있는데 api에 요청 날릴 때 좀 뭐랄까 명확하지 않게 전송되는거 같아서 
이 부분은 제외했다. 끝!

*****
### 3주차 미션: DRF1 - Serialize, API 설계

#### - serializes.py

     class TodoSerializer(serializers.ModelSerializer):
         user_name = serializers.SerializerMethodField()
         goal_name = serializers.SerializerMethodField()
         todo_like = serializers.SerializerMethodField()

         class Meta:
             model = Todo
             fields = ['user', 'goal', 'content', 'date', 'state', 'like_count',
                       'user_name', 'goal_name', 'todo_like']

         def get_user_name(self, obj):
             return obj.user.username

         def get_goal_name(self, obj):
             return obj.goal.name

         def get_todo_like(self, obj):
             return list(Like.objects.filter(todo_id=obj.id).prefetch_related('like_todo').values())

> 상세적인 내용을 직접 정의할 필요가 없는 ModelSerializer 사용,
> nested가 아닌 method 방식이 더 빠르다 하여 사용,
> 추후 serialize 데이터 변경이 있을지 몰라 fields에 명시,
> dto와 비슷한 느낌 받음,

#### - views.py
     
     class UserViewSet(viewsets.ModelViewSet):
         serializer_class = UserSerializer
         queryset = User.objects.all()

         def destroy(self, request, *args, **kwargs):
             user = self.get_object()
             user.is_active = False
             user.delete()
             user.save()
             return Response(data='delete user success')
             
> 간단한 로직이라 viewset 사용 및 soft delete사용으로 destory override 함 (상태변화)

#### - 데이터 출력

     # api.models.py
     class Todo(BaseModel):
         user = models.ForeignKey(User, related_name='todo_user', on_delete=models.DO_NOTHING)
         goal = models.ForeignKey(Goal, related_name='todo_goal', on_delete=models.DO_NOTHING)
         content = models.CharField(max_length=100)
         date = models.DateTimeField(default=timezone.now, help_text="날짜 및 시간")
         state = models.BooleanField(default=False)
         like_count=models.PositiveIntegerField(default=0)


<img width="452" alt="스크린샷 2022-10-07 오후 7 40 51" src="https://user-images.githubusercontent.com/62806067/194535327-928b0b57-3026-409d-9750-717d28b21d9c.png">

#### - 모든 데이터 조회 api

     GET 127.0.0.1:8000/api/todo/
     
Json 결과 값

<img width="394" alt="스크린샷 2022-10-07 오후 7 14 33" src="https://user-images.githubusercontent.com/62806067/194530842-397daffb-05ba-4da4-b3fb-58d56d63ee4d.png">

#### - 특정 데이터 조회 api

     Get 127.0.0.1:8000/api/todo/1
     
Json 결과 값

<img width="323" alt="스크린샷 2022-10-07 오후 7 16 54" src="https://user-images.githubusercontent.com/62806067/194531449-0aa93586-2e28-47d9-9a4e-6cb23e4b65cf.png">

#### - 데이터 추가 요청 api

     Post 127.0.0.1:8000/api/todo
     
Json 결과 값


<img width="500" alt="스크린샷 2022-10-07 오후 7 21 15" src="https://user-images.githubusercontent.com/62806067/194532048-4290b3e5-802d-4d8a-87ae-7e78d534c6b3.png">



#### - 데이터 삭제 요청 api

Json 결과 값

<img width="500" alt="스크린샷 2022-10-08 오전 1 45 33" src="https://user-images.githubusercontent.com/62806067/194605429-4fb52a3a-cb02-4efa-8aca-32eaa83520e6.png">

상태 변화 확인

<img width="308" alt="스크린샷 2022-10-08 오전 1 45 56" src="https://user-images.githubusercontent.com/62806067/194605459-2ea82f65-26d3-4e70-b961-d90679f8d6f2.png">

#### - 총평

1. 이번에도 역시 뭐가 맞는지 몰라 열심히 찾아봤다. 스프링이랑 비슷한가? 싶을 때 쯤 다른게 느껴진다.
2. 편하다는거 막 가져다 쓸라니까 힘들었다. 편하다고 만들어주긴했는데 좀 명시적으로 만들어 주면 좋았을텐데 싶었다 너무 지맘대로 이름을 정한기분
3. list랑 detail을 구분한다는게 요상했다. 매우.
4. 나름 열심히했는데 잘한건지 모르겠당.

*****
### 2주차 미션: DB 모델링 및 Django ORM
#### - ERD 설계 
<img src="https://user-images.githubusercontent.com/62806067/193407054-74253a1b-49ed-47fa-ba48-b622a057e3d2.png" width="800" height="400"/>

> 기초적인 기능 중심으로 설계
1. user : Django에서 기본적으로 제공하는 모델이 아닌 확장해서 사용 할 수 있는 Abstract 모델을 사용함으로 써 필요한 부분만 가져다 씀
2. goal : 목표 테이블로 todo의 카테고리 기능을 함, 공통 목표가 아닌 사용자 별로 원하는 목표가 다르므로 user을 fk로 가진 테이블을 생성
3. todo : todo 테이블로 할일이 등록되는 테이블, user와 goal을 fk로 가지고 있으며 content에는 내용, date에는 해당 날짜가 들어갈 것
4. like : 좋아요 기능을 구현하기 위한 테이블, todo와 user을 fk로 가지고 잇음
* basemodel : 생성시간, 수정시간, 삭제시간, 삭제여부 필드가 있으며 모든 테이블이 해당 모델을 사용함

#### - models.py 구현 및 migratiob
models.py 일부 발췌

     # api.models.py
     class Todo(BaseModel):
        user = models.ForeignKey(User, related_name='todo', on_delete=models.DO_NOTHING)
        goal = models.ForeignKey(Goal, related_name='todo', on_delete=models.DO_NOTHING)
        content = models.CharField(max_length=100)
        date = models.DateTimeField(default=timezone.now, help_text="날짜 및 시간")
        state = models.BooleanField(default=False)
        like_count=models.PositiveIntegerField(default=0)


> delete를 따로 설정해줘서 on_delete=models.DO_NOTHING 사용, datetime 특정 warning으로 timezone.now 사용

마이그레이션 코드

    python manage.py makemigration
    python manage.py migrate


#### - ORM 사용

<img width="600" alt="orm1" src="https://user-images.githubusercontent.com/62806067/193408520-a8555eb8-b421-4c7b-a591-7966d62dc29e.png">

> User, Goal 두개의 fk를 가지는 Todo에 3개의 객체를 집어넣음  

<img width="600" alt="orm2" src="https://user-images.githubusercontent.com/62806067/193408562-f85956ee-de0d-4a7b-9ca3-a211b6db0810.png">

> Todo를 query와 함께 queryset으로 보여줌

<img width="600" alt="orm3" src="https://user-images.githubusercontent.com/62806067/193408568-d89fd2e8-f0a0-4e75-9a17-54742c4fab6b.png">

> 다른 Goal 생성 후 Todo에 filter을 사용해서 조회함, Goal별로 조회 


#### - 총평

1. abstractuser 가 정확히 뭔지 몰라서 한참 찾았다. 애초에 만들기 전에 해주면 좋대서 했는데 아직 뭐가 그렇게 다른지 체감이..
2. enum이 text로 들어가서 제대로 조회가 안된다고 한다. 그러니까 새로 만들어 줘야하는데 여기까진 시간이 없어서 아쉬웠다.
3. 추가적인 기능을 구현할만한게 뭐가 있는지 고민했는데 워낙 단순한 서비스라 더 할게 없었다. - 굳이 해주자면 알람정도?
4. 이번엔 env로 보안 처리도 잘해주고 db도 바꿔보고 삽질과 함께 이것 저것 해봐서 재밋었다.. 나름... :)
