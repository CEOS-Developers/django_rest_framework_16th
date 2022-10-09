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
<<<<<<< HEAD
책 좀 읽고 공부해야겠다!

---

## 3주차 미션 : DRF1 - Serializer 및 API 설계
### 데이터 구조 수정
%erd 사진

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
%데이터 삽입 사진 2장

- 추가된 데이터 
  - Category: study, play 
  - Todo: django study, code review, lets go sinchon
- mysql로 확인

  %mysql 사진

### 모든 데이터를 가져오는 API
- URL: api/todo
- METOD: GET

### 특정 데이터를 가져오는 API
- URL: api/todo/<int:pk>
- METOD: GET

### 새로운 데이터를 create하도록 요청하는 API
- URL: api/todo
- METOD: POST
- BODY
  ```json
  {
    "user": "유저 ID",
    "category": "카테고리 ID",
    "content": "TODO 내용"
  }
  ```

  deadline을 지정하지 않아도 괜찮지만 models.py에서 field와 default의 데이터 타입을 다르게 설정하여 에러가 나 이번에만 설정해주었다. 추후에 수정 예정
  
### 특정 데이터를 삭제 또는 업데이트 하는 API
####삭제
- URL: api/todo/< int:pk >
- METOD: DELETE

####업데이트
- URL: api/todo/< int:pk >
- METOD: PUT
- BODY
  ```json
  {
    "user": "유저 ID",
    "category": "카테고리 ID",
    "수정을 원하는 필드"
  }
  ```
  
  user와 category를 body 추가하지 않고 api를 요청하였더니 필수값이라고 에러가 났다. 안해도 상관 없는 것으로 아는데 확인 필요!
### 에러 해결
- BaseModel의 created_at

  %created_at error 사진 1

  이때 created_at에 그냥 auto_now_add=True만 지정해주면 다음과 같이 default를 추가하라는 메시지가 나온다.

  %created_at error 사진 2

  그래서 default를 지정해주면 둘 중에 하나만 쓰라고 에러 메시지가 출력되어 null=True을 추가하여 우선 해결해주었다.

- DELETE
  
  %DELETE 에러 사진 
  ```
  TypeError: __init__() missing 1 required positional argument: 'data'
  ```
  에러가 나지만 DB를 확인해보면 어찌됐든 지워져 있었다. 구글링해봐도 잘 모르겠어서 더 찾아보고 수정해야 한다.

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

=======
책 좀 읽고 공부해야겠다! 그리고 좋아요 기능이 있다는걸 나중에 알아서 추가를 못했는데 후에 수정해야 한다.
>>>>>>> origin/geniee44
