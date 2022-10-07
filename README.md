# CEOS 16기 백엔드 스터디 : TODO_MATE

### 3주차 미션: Serialize, API 설계
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


<img width="600" alt="스크린샷 2022-10-07 오후 7 21 15" src="https://user-images.githubusercontent.com/62806067/194532048-4290b3e5-802d-4d8a-87ae-7e78d534c6b3.png">


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
