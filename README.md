# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포


## 2주차 미션: DB 모델링 및 Django ORM

투두메이트(TodoMate) 서비스
 - 투두메이트 서비스는 간단하게 내가 할 일에 대해서 설정하고, 이에 대해서 정보를 등록하고 확인하는 방식으로 생각했습니다.
 - 또한 각 유저별로 자신이 해야하는 todo list가 다를 것이기 때문에, 이를 생각하며 모델링을 진행했습니다.

모델링 결과
 - Profile Model : User에 대한 모델
   - user : OneToOne 방식으로 user의 방식을 확장함
   - image : 유저의 프로필 사진을 등록
   - nickname : 유저의 닉네임을 등록
   - message : 유저의 상태명을 등록
 - TodoList Model : Todo List에 대한 모델
   - profile : 유저에 대한 정보
   - description : 유저가 해야하는 to do list에 대한 설명
   - created_date : 작성일


1. **데이터베이스에 해당 모델 객체 3개 넣기**
<img width="731" alt="스크린샷 2022-10-01 14 40 49" src="https://user-images.githubusercontent.com/56791347/193398640-f1217ebd-b42c-4d2d-b3aa-7c5aae065ad2.png">
<img width="843" alt="스크린샷 2022-10-01 14 40 58" src="https://user-images.githubusercontent.com/56791347/193398644-c5a2f2b1-b89d-4d43-9ef4-80c4a199a4a5.png">
<img width="754" alt="스크린샷 2022-10-01 14 47 51" src="https://user-images.githubusercontent.com/56791347/193398650-4aa732f1-9daf-43b5-811f-2cb823949632.png">
<img width="680" alt="스크린샷 2022-10-01 14 47 59" src="https://user-images.githubusercontent.com/56791347/193398656-ad7a7bf5-87d4-4a04-92f2-ea66c675f4b1.png">
<img width="973" alt="스크린샷 2022-10-01 14 48 07" src="https://user-images.githubusercontent.com/56791347/193398662-a19006ef-5e05-430d-9884-8c8fcf82f593.png">

2. **삽입한 객체들을 쿼리셋으로 조회해보기 (단, 객체들이 객체의 특성을 나타내는 구분가능한 이름으로 보여야 함)**
<img width="945" alt="스크린샷 2022-10-01 16 54 27" src="https://user-images.githubusercontent.com/56791347/193399301-c499fdf5-20ec-4de5-b87e-4793665e5d76.png">

3. **filter 함수 사용해보기**
<img width="791" alt="스크린샷 2022-10-01 14 49 04" src="https://user-images.githubusercontent.com/56791347/193398670-63b6989c-0d2d-45b7-ad82-d9884afacf13.png">

🤍**간단한 회고**🤍  
1. 음...모델링하는거 생각보다 어렵다.. 학부생때도 모델링하는거에 익숙치 않았음 + 다 까먹음의 콜라보인데, 막상 다시 하려니까 제대로 한 것인지도 모르겠고 바보가 된 것 같은 느낌이다!
갑자기 난이도가 확 올라간 느낌이라 좀 많이 당황해서.. 계속 내가 제대로 한 것인지 모르겠다라는 생각뿐이다..
사실 학부생때는 백엔드 공부는 깨짝깨짝 해보고, 네트워크 및 인프라 공부만 했어서 이런 모델링 부분은 처음이지만 다른 백엔드 파트분들의 모델링을 보면서 공부해봐야할 것 같다.

3. 아직 나는 말하는 감자인듯..하다..🥔 열심히 살아야겠다..