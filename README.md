# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포

## Todomate
### Todomate란?
일정 관리 + 타인과 일정 공유
### 기능
1. 해야 할 일을 목표별로 나눠 저장
2. 일기 작성 가능
3. 팔로워와 자신의 일정을 공유하고, 일기와 할 일에 관해 좋아요(이모지)를 남길 수 있음

## ERD
![erd](https://user-images.githubusercontent.com/67852689/193394096-e3eb8f21-4188-4e33-9e26-6d47784dd5ba.jpeg)
* User : Django의 유저모델과 OneToOne 확장 이용, 유저의 정보를 저장
* Goal : 목표에 대한 정보를 저장, 1(User) : N(Goal), 1(Goal) : N(Todo)
* Todo : 투두에 관한 정보를 저장, 1(Goal) : N(Todo)
* TodoLike : 투두의 좋아요 정보를 저장, 1(Todo) : N(TodoLike), 1(User) : 1(TodoLike)
* Diary : 일기에 관한 정보를 저장, 1(User) : N(Diary)
* DiaryLike : 일기의 좋아요 정보를 저장, 1(Diary) : N(DiaryLike), 1(User) : 1(DiaryLike)
* Follow : 팔로우 관련 정보를 저장, 1(User) : N(Following)

## migration
```shell
python manage.py makemigrations api
python manage.py migrate api
```
* makemigrations : 모델을 변경시킨 사실 또는 새로 생성한 모델들과 같은 변경사항을 migrations로 저장
* migration : Django가 모델의 변경사항을 저장

