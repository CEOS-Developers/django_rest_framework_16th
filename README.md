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


models.py 작성 끝나면 migration!
```
python manage.py makemigration
python manage.py migrate
```
### ORM 이용해보기
1. 데이터베이스에 해당 모델 객체 3개 넣기
2. 삽입한 객체들을 쿼리셋으로 조회해보기 (단, 객체들이 객체의 특성을 나타내는 구분가능한 이름으로 보여야 함)
3. filter 함수 사용해보기

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
