# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포


## 2주차 미션: DB 모델링 및 Django ORM

## 투두메이트
일정 관리(투두리스트) 서비스.  
다른 사용자들에게 자신의 투두리스트를 공유할 수 있다는 차별점이 있다.  
서로 좋아요 등을 남길 수도 있고, 그래서 더 동기부여가 된다!

## 모델 설계

### User
django에서 기본 제공하는 user 모델 상속  - AbstractUser를 상속받아 custom함
- email을 유저네임으로 사용하도록 custom

### Friends
- user: Profile을 참조하는 foreign key
- subscription: user가 팔로우하는 친구들의 이메일이 저장됨.

### Category
- category_name: 카테고리명
- user : Profile을 참조하는 foreign key, 어떤 사용자의 카테고리인지 보여줌

### Todo
- todo_name: to do item을 작성했을 때 그것의 이름
- user: 작성한 사용자
- category: 카테고리
- public: 친구들에게 공개할 것인지 여부, private(비공개), only friends(친구 공개), public(전체 공개) 중 선택할 수 있도록 한다.  
default는 public(전체공개)
- date: 일정별 to do list를 볼 수 있도록

### Communication
- todo: Todo를 참조하는 foreign key, 어떤 to do item에 대한 활동인지 보여줌
- author: Profile을 참조하는 foreign key, 작성자
- emoji: 한 글자짜리 이모티콘으로 반응
- comment: 서로 댓글을 달 수도 있다.

## ORM 이용해보기

## 이번 과제를 하며..

