# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포

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
