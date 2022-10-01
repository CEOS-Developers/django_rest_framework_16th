# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포


## 2주차 미션: DB 모델링 및 Django ORM

## Todo Mate 기능
- 날짜별 할 일 추가 및 관리
- 이모지, 사진을 이용한 오늘 하루 일기 작성
- 서로 팔로우하며 친구의 일정, 일기에 좋아요 응원 

## erd
#### User
![User](file:///Users/chaeseunghui/Desktop/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-10-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2010.51.40.png)
#### Todo
![Todo](file:///Users/chaeseunghui/Desktop/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-10-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2010.54.08.png)
- user와 1:N 관계 : foriegn key로 user 지정
- date 입력 형식 지정
#### Diary
![Diary](file:///Users/chaeseunghui/Desktop/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-10-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2010.55.56.png)
- user와 1:N 관계 : foriegn key로 user 지정
- date 입력 형식 지정
- 비공개 여부 private BooleanField 사용
#### Likes
![Likes](file:///Users/chaeseunghui/Desktop/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-10-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2010.57.42.png)
- 유저(User)-좋아요 1:N 관계 : foriegn key로 유저 지정
- 유저 - 좋아요 - 할 일 N:M 관계 -> ManyToMany
- 유저 - 좋아요 - 일기 N:M 관계 -> ManyToMany
#### Follows
![Follows](file:///Users/chaeseunghui/Desktop/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-10-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2011.01.48.png)
- 맞팔로우 서로 N:M 관계 -> ManyToMany

## ORM
- ForiegnKey 필드를 포함하는 Todo 모델 객체 생성
![ForiegnKey로 사용될 User 객체 생성](file:///Users/chaeseunghui/Desktop/1-%E1%84%83%E1%85%B5%E1%84%87%E1%85%B5.png)
![Todo 모델 객체 생성](file:///Users/chaeseunghui/Desktop/1.png)
![Todo table](file:///Users/chaeseunghui/Desktop/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-10-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2011.07.49.png)
- ORM 쿼리셋 조회
![Query](file:///Users/chaeseunghui/Desktop/2.png)
- filter 사용
![filter](file:///Users/chaeseunghui/Desktop/3.png)

## 마무리하면서..
mysql 사용부터 migration을 하는 과정에서 에러가 많이 떠서 해결하는데 고생을 했다... 과제도 이전보다 난이도가 많이 높아져서 어려웠지만 1대다 관계, 다대다 관계등을 고민해보고 erd를 짜면서 각각 모델이 어떻게 연결되는지 이해할 수 있었다. 기억나는 에러사항은 
1. m1 환경에서는 settings.py에 pymysql을 다운받고 import하여 pymysql.install_as_MySQLdb()를 작성해주어야한다.
2. 원하는 날짜를 객체의 field값으로 넣어주고 싶을 때 input_format으로 형식으로 지정해줄 수 있다.
그리고 알게된 점은 
- CharField를 사용하고자 할 때는 max_length 값을 필수로 지정해준다.
- timezone으로 정확한 날짜와 시간을 사용하고자 한다면 setting에서 TIME_ZONE을 서울로 설정해준다.
- 원하는 형태로 객체를 확인하려면 def __str__(self)에서 리턴값을 설정해준다.
등이 있었다. erd를 완성하고 나서 실제 서비스를 구현하려면 더 세분화해서 모델을 작성했어야겠다는 생각이 들었다. 다음 스터디에서 피드백을 통해 erd를 더 발전시킬 수 있길...

