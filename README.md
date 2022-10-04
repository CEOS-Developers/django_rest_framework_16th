# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포

## Todomate
### Todomate란?
일정 관리 + 타인과 일정 공유
### 기능
1. 해야 할 일을 목표별로 나눠 저장
2. 일기 작성 가능
3. 팔로워와 자신의 일정을 공유하고, 일기와 할 일에 관해 좋아요(이모지)를 남길 수 있음

## ERD
![CEOS - TODO](https://user-images.githubusercontent.com/67852689/193405189-b74861af-5b2b-4a47-ada6-b8e8a37a730c.png)
* Profile : Django의 유저모델과 OneToOne 확장 이용, 유저의 정보를 저장
* Goal : 목표에 대한 정보를 저장
  * 1(User) : N(Goal) : 유저가 여러 개의 목표를 생성할 수 있다.
  * 1(Goal) : N(Todo) : 한 목표에 여러 투두를 생성할 수 있다.
* Todo : 투두에 관한 정보를 저장
  * 1(Goal) : N(Todo)
* TodoLike : 투두의 좋아요 정보를 저장
  * 1(Todo) : N(TodoLike) : 한 투두에 많은 수의 좋아요를 가질 수 있다.
  * 1(User) : 1(TodoLike) : 한 명의 유저가 좋아요 하나만 남길 수 있으므로 1 대 1이다.
* Diary : 일기에 관한 정보를 저장
  * 1(User) : N(Diary) : 일기를 날짜별로 적을 수 있다. 그러므로 유저 한 명은 여러 개의 일기를 적을 수 있다.
* DiaryLike : 일기의 좋아요 정보를 저장
  * 1(Diary) : N(DiaryLike) : 일기도 투두와 마찬가지로 많은 수의 좋아요를 가질 수 있다.
  * 1(User) : 1(DiaryLike) : Todo 좋아요와 이유는 동일하다
* Follow : 팔로우 관련 정보를 저장
  * 1(User) : N(Following) : 한 유저와 많은 수의 유저가 팔로우 관계를 맺을 수 있다.

## migration
```shell
python manage.py makemigrations api
python manage.py migrate api
```
* makemigrations : 모델을 변경시킨 사실 또는 새로 생성한 모델들과 같은 변경사항을 migrations로 저장
* migration : Django가 모델의 변경사항을 저장

## ORM 사용해보기
![image](https://user-images.githubusercontent.com/67852689/193402878-b9dd40d1-ad7b-4a91-9161-ef7e1d41a918.png)
> 유저 모델 객체 3개

![image](https://user-images.githubusercontent.com/67852689/193402877-da27e1b4-ca98-4622-8f2f-517e256dd3fd.png)
> 유저 테이블 인스턴스를 외래키로 가지는 인스턴스를 생성 및 조회

![image](https://user-images.githubusercontent.com/67852689/193402880-cea2dcf2-65ae-4b6b-8ac3-997a42fd9007.png)
> filter를 이용해 조회

## 회고
1. django.db.utils.IntegrityError: (1048, "Column 'user_id' cannot be null")<br>
Profile 인스턴스를 만들면 User가 자동으로 생성되는 줄 알았으나, 아니었다. 장고는 User를 자동적으로 생성해 주지 않기 때문에, Profile 인스턴스를 만들기 위해선,
먼저 User 인스턴스를 만들어줘야 한다.
2. MySQLdb.ProgrammingError: (1146, "Table 'todo.api_profile' doesn't exist")<br>
결론부터 말하자면, 디비 문제였다. User 테이블의 이름을 Profile로 바꾸면서 디비에 저장되어 있던 데이터와 코드에 적혀있는 모델과의 차이 때문에 발생했던 것 같다.
디비를 초기화하고 migration 파일을 모두 삭제해서, 문제를 해결할 수 있었다.
3. 어렵다<br>
그래도 프론트보단 좋다ㅋ