

# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포


## 2주차 미션: DB 모델링 및 Django ORM

## 투두메이트 모델링

평소에 매일 사용하는 어플이라서 되게 간단할 줄 알았는데, 생각보다 고려해야할 부분이 많아서 조금 당황했다. . . 복잡하지는 않은 것 같은데 모델링을 처음 해보다 보니까 잘 한건지는 잘 모르겠다

![image](https://user-images.githubusercontent.com/80627536/193395496-ba0551d8-1ddb-43ec-9105-7e437760a810.png)

우선 간단히 설명을 하자면

 유저 모델은 
 
	1. 기본적으로 nickname(닉네임)이 있다. 투두메이트에서 남들이 볼 때 보이는 닉네임으로 가장 중요하다면 중요한 부분
	
	2. 당연하게도 username이랑 password, 그리고 email이 있고,
	
	3. profile_image는 있어도 그만 없어도 그만인 유저의 프로필 사진이다
	
	4. description은 유저의 상태메세지로 마찬가지로 있어도 그만 없어도 그만
	
	5. show_email이랑 show_search는 이메일 또는 랜덤 검색 기능으로 본인의 프로필이 보이길 바라냐는 선택지이다. True <-> False 의 선택지밖에 없으니 BooleanField로 지정을 했다.
	
	6. 나머지는 created_at, updated_at, deleted_at인데, created_at은 유저가 처음 계정을 생성한 타이밍으로 지정을 해주고, updated_at은 프로필이 변경될 때 시간이 업데이트가 되어야한다. 마지막으로 deleted_at은 있어야하나 고민을 좀 해봤는데, 최근에 서비스 런칭하려고 개인정보 관련해서 좀 찾아보니까, 6개월동안은 의무적으로 사용자의 정보를 보관해야한다고 하더라,,, 그래서 만약 유저가 탈퇴를 하고싶어하면 바로 유저를 삭제하는게 아닌, deleted_at을 통해서 삭제된 유저인지 아닌지를 판단해야한다. 
	

![image](https://user-images.githubusercontent.com/80627536/193395736-6862becc-f796-4fdf-a235-543320f8ef6f.png)

다음으로 중요한건 투두의 분류이다.
투두의 분류 (TodoClass)는

	1. user_id를 FK로 갖는다. 한명의 유저가 여러개의 TodoClass를 가질 수 있기에 1:N 관계이다. 
	
	2. class_name은 TodoClass의 보여지는 이름
	
	3. class_color는 투두메이트에서 각 투두 분류마다 색깔이 있는데, 그 색을 설정해주는 부분이다. CharField로 지정한 이유는 "#ffffff"이런식으로 받는게 좋지 않을까 해서 그렇게 했는데, 다른 좋은 방법이 있는지는 잘 모르겠다. . . ColorField라는게 있는 것 같기도 한데, pip를 통해서 설치를 해야하는거보면 뭔가 지금 당장 필요한 건 아닌 것 같다.
	
	4.  is_open은 이 특정 TodoClass가 남들에게 보였으면 하냐 안하냐인데, BooleanField로 하지 않은 이유는 선택지가 세개이기 때문이다. 나만 공개도 있고, 친구 공개도 있고, 전체 공개도 있어서, 0 1 2 값으로 구분을 하는게 좋겠다 싶어서 IntegerField로 했다. 
	
	5. created_at, updated_at, deleted_at은 유저 모델과 동일하다

![image](https://user-images.githubusercontent.com/80627536/193395875-ae8f7e1d-b75f-4371-8c21-7f3e071e5c6c.png)

다음은 대망의 Todo!

Todo는

	1.  User의 id값과 TodoClass의 id값을 FK로 갖는다. 
	
	2. 한명의 유저는 여러개의 투두클래스와 투두를 가질 수 있고, 한개의 투두 클래스는 여러개의 투두를 가질 수 있기 때문이다
	
	3. title은 투두의 제목이다. 
	
	4. is_finished는 이 투두를 했는지 안했는지를 구분하는데, 두가지의 선택지밖에 없기 때문에 BooleanField를 이용했다.
	
	5. picture는 가아아끔 투두 사진 인증을 위한건데, ~~쓰는 사람을 본적이 없다~~ 
	
	6. is_default는 이 투두가 매일 하는 투두인지 아닌지를 구분하는 값이다. 
	
	7. created_at, updated_at, deleted_at은 유저 모델과 동일하다
	

![image](https://user-images.githubusercontent.com/80627536/193396186-b21a9a4c-608d-450c-9bb9-0f1f5a4a3138.png)


TodoLike도 사실 투두메이트의 핵심이다. 좋아요가 없으면 투두메이트를 쓸 이유가 없다!

TodoLike는

	1. User 본인의 id 값, 투두의 id값, 그리고 상대방 user의 id값 세가지를 FK로 갖는다. 
	
	2. 사실 가장 어려웠던 부분인데, 1:1인지 1:N인지 N:M인지를 잘 모르겠다. . . 한명의 유저는 여러개의 투두 좋아요를 누를 수 있고, 한개의 투두는 여러명한테 좋아요를 받을 수 있다. 그러면 N : 1 : M? ? 이런게 있나...? 조오금 헷갈린다. . .
	
	3. emoji는 어떤 이모티콘으로 좋아요를 눌렀는지를 구분하는 값이다
	
	4.  created_at, updated_at, deleted_at은 유저 모델과 동일하다

![image](https://user-images.githubusercontent.com/80627536/193396195-f4d57a04-ece5-40af-920d-5e52febb1dd8.png)


다음 두개의 모델은 일기 모델과 일기 좋아요 모델인데, 
처음에는 고민을 좀 했다.. 써본적 없는 기능인데 이거를 할 필요가 있나? 라는 생각이 처음에는 들었지만, 생각을 해보니 앞으로 모델링을 할 때 꼭 내가 써본 기능만 모델링을 하는게 아니겠구나 라는 생각을 해서 바로 모델링을 했다. 
근데 확실히 써보지 않은 기능이라서 조금 더 생각을 많이 해야했다. 

우선 Diary 모델은

    1. User의 id값을 FK로 갖는다. 한명의 유저는 여러개의 일기를 쓸 수 있기 때문이다. 
    
    2. content는 이 일기의 내용인데, 최대 값을 그냥 한 500정도로 지정을 하긴 했지만, 조금 부족할 수도 있지 않을까 싶기는 하다. 
    
    3. bg_color는 이번에 일기 기능을 보면서 알게된 기능인데, 일기의 배경 색을 지정해줄 수가 있더라. . . 그래서 넣었다. 
    
    4. picture는 일기의 사진을 넣을 수 있기 때문에 필요하다
    
    5. emoji는 이 일기를 쓰는 날의 기분을 표현하는 느낌? ? 
    
    6. temperature는 살짝 emoji랑 역할이 겹치는 것 같아서 생각을 좀 했는데, emoji는 다른 사람들이 한번에 볼 수 있게, 그리고 한달 전체의 기분을 대충 파악할 때 도움이 될 것 같고, temperature는 emoji로는 표현할 수 없는 자세한 기분의 온도를 적을 수 있어서 있어야 할 것 같았다. 
    
    7. is_open은 TodoClass의 is_open처럼 이 일기가 다른 사람들한테 보이는지 안보이는지를 지정해주는 값이다.
    
    8.  created_at, updated_at, deleted_at은 유저 모델과 동일하다

![image](https://user-images.githubusercontent.com/80627536/193396463-492a9489-2d6a-4750-b58d-8109d21155a3.png)


마지막으로 DiaryLike 모델이다.
1. 일기에 좋아요를 누르는건 사실 투두에 좋아요를 누르는거랑 완전히 똑같은 기능이더라. 그래서 TodoLike 모델을 그대로 가져와서 이용했다. 

![image](https://user-images.githubusercontent.com/80627536/193396481-2564edc1-6382-4fe7-99a7-7b116f6b9050.png)



## Database Query

우선 생성한 DB에 제대로 모델들이 생성이 됐는지를 확인해보자

mysql -u root -p 를 치고 비밀번호를 치면 mysql에 접속을 할 수 있고, 
그리고 use "DB명" -> show tables; 를 하면 

![image](https://user-images.githubusercontent.com/80627536/193398661-a6db813a-a4aa-49f3-b3dc-cedf300d56b0.png)

이렇게 생성되어있는 모든 테이블들을 볼 수 있고, 자세히보면 생성한 모델들이 다 적용이 된걸 확인할 수 있다. 


이제 shell을 통해서 데이터베이스에 데이터를 저장하고 확인을 해보자

1. 유저 생성
![image](https://user-images.githubusercontent.com/80627536/193398867-0e2717d5-69ab-418d-8f52-3d44bb75c919.png)
2. 유저를 filter를 통해서 확인
![image](https://user-images.githubusercontent.com/80627536/193398881-a1678bbe-0f8a-47cd-8635-22069658a7f3.png)


User를 FK로 갖는 TodoClass 생성하기

1. Nickname이 bokdol인 유저가 개인 공부라는 이름을 가진 TodoClass를 생성한다.

![image](https://user-images.githubusercontent.com/80627536/193399032-b860aa8e-6d8f-4c81-a837-b2ff2eeded87.png)

2. Nickname이 bokdol인 유저가 운동이라는 이름을 가진 TodoClass를 생성한다.

![image](https://user-images.githubusercontent.com/80627536/193399119-d88d3466-fafb-4a5a-8411-23cf7a94a01b.png)

 3. Nickname이 bokdol인 유저가 학교 공부라는 이름을 가진 TodoClass를 생성한다.
 
 ![image](https://user-images.githubusercontent.com/80627536/193399148-54b9071c-83f3-482d-8a1a-fc1fea2b679d.png)
 

세개의 TodoClass를 생성을 했으니, 제대로 생성이 됐는지를 확인을 해보자.

![image](https://user-images.githubusercontent.com/80627536/193399183-952dda9e-7f06-44c6-8536-afd9087f2083.png)
TodoClass.objects.all()을 통해서 모든 TodoClass를 가져왔고, QuerySet을 확인해보니 정상적으로 아까 생성한 세가지의 TodoClass가 저장이 되어있는걸 확인할 수 있다. 

조금 더 확실하게 Filter를 이용해보기 위해서 Todo를 하나 생성해봤다.

![image](https://user-images.githubusercontent.com/80627536/193399409-f5ee4175-73a8-4b50-ba27-3419443b0e1b.png)

이제 그럼 Todo 중에서 TodoClass가 "개인 공부"이고 User가 "bokdol"인걸 Filter해보자. 

![image](https://user-images.githubusercontent.com/80627536/193399506-3e9e5670-a09a-4a56-b51e-8ceb7f28e217.png)

뭔가 Filter 하는게 분해는 조립의 역순인 것 마냥 그대로 따라친 것 같기는 한데, 일단 정상적으로 Todo를 Filter하는걸 확인할 수 있다. 근데 뭔가 너무 야매같아서 Todo를 하나만 더 생성해보고 걸러지는지 확인해보자.

"ceos"라는 닉네임을 가진 유저가, "운동"이라는 TodoClass에 " \*오운완\* ^^7 "이라는 투두를 생성을 했다. ~~마땅히 떠오르는게 없어서 막 적었는데 좀 창피하다~~

아무튼 이렇게 두개의 Todo가 생성이 됐으니, TodoClass 이름을 기준으로 Filter가 제대로 동작하는지 한번 확인해보자.

![image](https://user-images.githubusercontent.com/80627536/193399683-b106d1d3-70d6-4672-90ef-5d9e12c64c9f.png)


각 조건에 맞게 Todo를 Filter하는 것을 확인할 수 있다. 




## 회고

살면서 처음으로 모델링이라는 것을 해봤다. . . 사실 저번 과제에 비해 갑자기 난이도가 확 올라간 느낌을 받아서 조금 당황했는데, 막상 하다보니까 재밌어서 금방 했던 것 같다... 물론 완성도나 정확도는 보장 못합니다..

사실 프론트엔드 개발을 하면서 가끔 백엔드에서 왜 도대체 api를 이런식으로 쏴주지? 하는 경우가 좀 많았는데, 반성하게 된 것 같다... 백엔드 어렵다... 

되게 쉽게 생각했던 투두메이트도 알고보니 엄청 복잡한 구조를 갖고 있었는데, 진짜로 복잡한 서비스들은 그럼 얼마나 더 복잡한건지 상상이 안간다.. 나 백엔드 할 수 있을까...?

그리고 강의나 그런거 들으면서 ORM ORM QUERY QUERY 이런 단어들을 너무 많이 들어서 막 구글링 해봐도 정확한 의미는 잘 몰랐는데, 확실히 사용해보니까 바로 뭔지 알 것 같더라. 

> **백문이 불여일타**

프로그래밍은 절대 이론만 공부해서는 되는게 아니라는 걸 다시 한번 깨닫게 됐다. 

저번 과제는 옛날에 그래도 비슷한걸 몇번 해봐서 수월하게 할 수 있었는데, 이번 과제는 진짜 조금 어려웠다... 과제하려고 책상에 앉아서 과제를 읽는 순간 머리가 하얘지면서 뭘 해야할지를 모르겠더라.. 그래도 아이패드를 꺼내서 하나씩 차근차근 적으면서 하다보니까 뭐라도 된듯

이번 과제 피드백을 통해서 모델링을 제대로 한건지 아닌지를 조금 더 배울 수 있을 것 같고,  이번 과제는 진짜로 백엔드 개발하는 느낌이 났어서 정말 재밌었다!! 다음 과제도 기대가 된다!



## 3주차 미션: DRF1: Serializer

이번 과제는 내가 가장 기대했던 과제이다. 그 이유는 백엔드에서 프론트엔드로 데이터를 보내줄 때의 방식들을 배울 수 있을거라고 생각했기 때문이다. 아니나 다를까, 역시 가장 재밌는 과제였다. ~~기왕 하는거 프론트도 개발해볼까 했는데 리소스 부족으로 실패,,,~~ 

근데 사실 맞게 한건지는 모르겠다. 분명 뭔가를 빼먹고 있는 것 같은데, 뭔지를 잘 모르겠다,,, 그리고 생각보다 방식이 정말 다양하더라.. 근데 분명 현업에서 가장 많이 쓰이는 방식이 있을텐데, 어떤건지를 잘 모르겠다.. 쓰다보면 알게되겠지

아무튼 저번 과제의 연장선이기 때문에, 저번에 만들었던 모델들을 이용했고, 조금 틀렸거나 아쉬웠던 부분들은 수정을 했다. 

이번 과제에서 중점적으로 이용한 모델은

 1. 투두클래스
 2. 투두

이렇게 두가지이다. 

## 1. 데이터 삽입

![image](https://user-images.githubusercontent.com/80627536/194548738-2fdfbae9-0839-43b3-80e8-f36cdfba1c06.png)


유저는 세개를 생성을 했고,

![image](https://user-images.githubusercontent.com/80627536/194549065-cd85e572-d796-401b-902f-5fff021e9076.png)

투두 클래스는 네개,

![image](https://user-images.githubusercontent.com/80627536/194549419-0bd4cb08-2af5-4789-908d-82ef69d48b73.png)

투두도 네개를 생성했다.


## 2. 모든 데이터를 가져오는 API 만들기

사실 어떤 데이터를 자주 한꺼번에 가져오게 될까를 고민해봤는데, 투두클래스, 투두 둘다 많이 쓰지 않을까 싶어서 결국 둘 다 만들었다. 

### 모든 투두클래스 가져오기
URL:  `v1/todo_classes/`
Method: `GET`

![image](https://user-images.githubusercontent.com/80627536/194550711-3742925f-14c9-44c4-860b-619b16b26aa2.png)



### 모든 투두 가져오기
URL:  `v1/todos/`
Method: `GET`

![image](https://user-images.githubusercontent.com/80627536/194550807-7427b3ae-7d24-4027-a740-87e5a8d0a388.png)

## 3. 특정 데이터를 가져오는 API 만들기

### 특정 투두 클래스 가져오기
URL:  `v1/todo_class/<int:id>`
Method: `GET`

![image](https://user-images.githubusercontent.com/80627536/194551280-d00ab871-efae-4f81-b374-17d8e62e0bde.png)


### 특정 투두 가져오기
URL:  `v1/todo/<int:id>`
Method: `GET`

![image](https://user-images.githubusercontent.com/80627536/194551378-fd740e4c-67db-4520-bb16-de5972235cd3.png)

## 4. 새로운 데이터를 create하도록 요청하는 API 만들기

### 새로운 투두 클래스 생성하기
URL:  `v1/todo_classes/<int:id>`
Method: `POST`

Request Body
![image](https://user-images.githubusercontent.com/80627536/194552641-6dd968c8-48c3-4b2b-b1b2-1574bb7710ee.png)

Response
![image](https://user-images.githubusercontent.com/80627536/194552700-ff3c4683-1abf-474c-b0e1-0dafc954f8d2.png)

### 새로운 투두 생성하기
URL:  `v1/todos/<int:id>`
Method: `POST`

Request Body
![image](https://user-images.githubusercontent.com/80627536/194553125-bd2032cf-b42c-4655-a3eb-b70e236987db.png)

Response
![image](https://user-images.githubusercontent.com/80627536/194553268-6a2435c6-1763-4822-9320-52c04a6a7b95.png)


## 5.  특정 데이터를 수정/삭제하는 API

### 특정 투두 클래스 수정하기
URL:  `v1/todo_class/<int:id>`
Method: `PATCH`

Request Body
![image](https://user-images.githubusercontent.com/80627536/194553931-53ffc971-c6bf-4819-ab0e-d1080f4063bd.png)

Response
![image](https://user-images.githubusercontent.com/80627536/194554066-709f92f3-a815-4f3e-b781-87fec201ade9.png)

### 특정 투두 클래스 삭제하기 (Soft-Delete)
URL:  `v1/todo_class/<int:id>`
Method: `PATCH`

Request Body
![image](https://user-images.githubusercontent.com/80627536/194554949-b70a0724-fc9c-4c7f-9521-17e883704ee6.png)

Response
![image](https://user-images.githubusercontent.com/80627536/194555020-1d4a9deb-ab15-4942-b230-bc56c406cd91.png)


### 특정 투두 수정하기
URL:  `v1/todo/<int:id>`
Method: `PATCH`

Request Body
![image](https://user-images.githubusercontent.com/80627536/194555553-1049de44-a555-4179-a79f-ff28cc5863cd.png)

Response
![image](https://user-images.githubusercontent.com/80627536/194555620-8a97c30b-4887-4796-9383-0aaa7b492422.png)


### 특정 투두 삭제하기
URL:  `v1/todo/<int:id>`
Method: `PATCH`

Request Body
![image](https://user-images.githubusercontent.com/80627536/194554949-b70a0724-fc9c-4c7f-9521-17e883704ee6.png)

Response
![image](https://user-images.githubusercontent.com/80627536/194555753-832039c9-8782-4d3b-99e3-a8ccbcbfa40e.png)

## 회고
진짜 진짜 재밌었다!
1, 2주차 과제도 백엔드 개발하는 것 같았어서 재밌었지만, 이번엔 진짜로 뭔가 백엔드 개발자가 된 느낌을 1% 받은 것 같아서 너무 재밌게 과제를 했다!

사실 이렇게 백엔드 API를 DRF로 만들어본적이 한번 있지만, 그때는 책을 따라 치기만 했기 때문에 내껄 만든다는 느낌도 없었는데, 이번에는 순도 100%는 아니고 사실 한 50%정도 내가 만든 느낌? 어쩌면 구글링이 한 60% 차지해서 내가 실제로 한건 40%도 안될지도,,,

아무튼 진짜 이번에는 내가 만든 것 같다는 느낌을 받아서 너무나도 재밌었다! ORM이 있으니까 DB에서 원하는 데이터를 뽑아내는게 훨씬 더 쉬워서 예상보다 더 수월하게 할 수 있었다. 

그래도 과제를 수행하면서 막히고 헷갈렸던 부분이 몇가지 있다. 

 1. POST 요청을 할 때에는 뭔가 당연히 /todo/로 POST 요청을 해야할 것 같은데, 사실 그렇게 하면 id값을 보내주지 않기 때문에 할 수가 없다.. 그래서 /todos/로 POST 요청을 보내야한다. 
 
 이건 사실 프론트엔드 개발자로 일을 할때에도 의문을 가졌던 부분이다. 왜 저렇게 하지?? POST 요청을 /todo/가 아니라 /todos/ 로 보낸다고?? 영어 문법상 뭔가 좀 이상한데? ? 라는 생각을 갖고 있었다... 이게 결국 아는 만큼 보인다고,,, 다 그런 이유가 있던 것이다... 
 
 2. Request Body에 데이터를 넣어서 보낼 때, 끝에 , 로 끝나면 오류가 난다...

이거는 진짜 위에 과제 사진 올리면서 계속 반복적으로 발생했던 오류다... 도대체 뭐가 문제지? ? 왜 어떨 땐 되고 어떨 땐 안되지? ?? 라는 생각을 하면서 한 30분을 고민했는데, 
진짜 간단한 이유였어서 조금 어이가 없었다,,

근데 사실 저게 맞는거 아닐까? ? 내가 그동안 너무 자동 디버깅에 익숙해져서 사소한 디테일들을 놓치고 있을 수도 있겠구나 라는 생각을 하게 되었다. . . 

아무튼 그렇습니다~! 너무나도 재밌게 했던 과제이고, 진짜로 백엔드 개발을 한 느낌이라서 백엔드 개발자로 한걸음 더 다가간 느낌이다! 만약 추후에 내가 백엔드 개발자를 하기로 선택을 한다면, 그 이유에서 이번 과제가 아주아주아주 큰 비중을 갖게 될 것 같다. 

사실 내년 초에 프론트엔드 개발자로 취업을 해야하는 상황이라 조금 고민을 많이 했고, 걱정도 많이 했다.. 프론트엔드 개발도 제대로 못하는 상황에서 백엔드 개발을 배우는건 너무 오만한 생각이 아닌가 싶었는데, 백엔드 개발 공부를 하면서 분명 취업에 도움이 되는 부분이 있을거라고 생각하기에 잡생각 말고 집중하기로 마음을 먹었다. 열심히 하겠습니다!


## 4주차 미션 : DRF2 - API View & Viewset & Filter

---


### 1. DRF API View 의 CBV로 리팩토링하기
![](https://velog.velcdn.com/images/bokdol11859/post/fdb113f9-327c-4ea5-917d-9b44f1b1e3d8/image.png)

상단에 있는 코드는 FBV, 하단에는 이번에 리팩토링한 CBV인데, 사실 뭐가 더 편한지는 모르겠다.. 둘다 비슷한 느낌?


### 2. Viewset으로 리팩토링하기

![](https://velog.velcdn.com/images/bokdol11859/post/1475f9ba-b32e-4580-8eaf-6f6ef9289227/image.png)

제대로 한게... 맞나 싶을 정도로 간단했는데, 사실 아직도 이게 맞게 한건지 모르겠다.. 분명 테스트를 해보니까 문제 없이 돌아가긴 하던데, 이렇게 간단해도 되는걸까 싶다


### 3. filter 기능 구현하기

![](https://velog.velcdn.com/images/bokdol11859/post/1c1cd505-c976-4b3e-a15d-6ae070bcd983/image.png)

TodoClass 를 GET 할 때 필터링을 걸어주기 위한 코드다.. 사실 필터링 부분에서 진짜 많이 해맸고, 아직도 해매는중인 것 같다.. 이게 왜 되지?? 원리가 너무 이해가 안된다.. 근데 과제는 제출해야하니까 일단 되는거만이라도 확인했다... 편하게 사용하려고 코드가 짧아지면 짧아질수록 초보자 입장에서는 이해가 하기가 더 어려운듯 하다.. 어떤 원리로 저게 되는건지는 조금 더 자세히 알아봐야할듯

![](https://velog.velcdn.com/images/bokdol11859/post/a178b1ae-9bd6-4d0f-8e5e-82f6cc053734/image.png)

일단 이렇게 쿼리를 날리면 알맞는 결과를 GET해올 수 있는 것을 확인할 수 있다. 사진상에서는 class_name이 운동이고, 모두에게 공개된 투두클래스를 가져올 수 있도록 쿼리를 날렸다.


![](https://velog.velcdn.com/images/bokdol11859/post/5b181f3d-e4e0-4cf5-8fdb-878d14f0530c/image.png)

마찬가지로 Todo를 GET할 때 필터링을 하기 위한 코드이다. 크게 다를건 없고, 끝난 투두인지 확인하는 부분이랑 투두 이름을 기반으로 필터링이 가능하도록 구현했다.

![](https://velog.velcdn.com/images/bokdol11859/post/1dcdc6ed-8725-4ba1-bd38-488b4e255869/image.png)

사진에서 확인할 수 있듯 완료되지 않은 투두중에서 이름에 하체가 들어간 투두를 가져오는 쿼리를 날렸고, 알맞게 데이터를 GET 해오는 것을 확인할 수 있다. 



## 회고

---

이번 과제는 조금 어려웠다.. 천재 개발자들이 편하게 쓰라고 막 다 줄여버리니까 나같은 초보자들은 이해조차 할 수가 없다,,, "아니 왜 저게 왜 저렇게? ?"라는 생각을 계속 가진 채로 과제를 한 것 같다.. ViewSet,,, FilterSet,,, 자세히 다시 공부를 해봐야할듯하다... 


# DRF3 : Simple JWT

---

간단 요약: 망했다. . . 어디서부터 잘못된걸까, , , 너무 어렵다


일단 뭐 어찌저찌 구현은 했으니까 적기 시작하겠습니다



### 로그인 구현하기

사실 로그인 기능을 구현하려면 회원가입도 같이 있어야 하지 않을까 싶어서 회원가입도 같이 구현을 했다. 그러니까 회원가입 먼저 얘기해보도록 하겠습니다

### 회원가입 구현하기

```

email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
)
password = serializers.CharField(
    write_only=True,
    required=True,
    validators=[validate_password],
)
password2 = serializers.CharField(write_only=True, required=True)

```

이메일 중복을 방지하기 위해서 UniqueValidator를 이용했고, 비밀번호 검증, 8자리 등등 그런 안전한 비밀번호 검증을 위해 django.contrib.auth.password_validation에서 validate_password를 이용했다. 그래서 비밀번호를 ceos16으로 하지 못하고 ceos1616으로 했습니다. . .

비밀번호를 다시 한번 쳐서 잘못 친걸 확인하기 위한 password2도 있고, 

![](https://velog.velcdn.com/images/bokdol11859/post/319d3f7f-8ac8-4f7d-985e-c12dc42cb7fe/image.png)

validate 함수를 통해서 두개가 일지하는지 안하는지를 확인하도록 했다.

이제 모든 값들이 정상적으로 입력이 된 input을 받았다고 가정을 하면, 

![](https://velog.velcdn.com/images/bokdol11859/post/36063a3e-6f9e-40d1-b63f-cdab5bdf1430/image.png)

이렇게 유저를 하나 생성하고, 그 유저의 token값을 생성하고 저장을 한다. 추후에 로그인을 하면 이 토큰 값을 반환할 예정

### 되나안되나테스트

![](https://velog.velcdn.com/images/bokdol11859/post/709a478c-2d6d-494b-a5c3-8edaac44d602/image.png)

닉네임은 ceos16, 유저네임도 ceos16, 비밀번호는 보안을 위해 ceos1616, 이메일은 ceos16@ceos.com으로 POST 요청을 보내면

닉네임, 유저네임, 그리고 이메일이 Response로 온다. 이렇게 온다는건 잘 생성이 됐다는 뜻이고, 만약 정보들이 중복된다면?

![](https://velog.velcdn.com/images/bokdol11859/post/ba9df1e2-1591-4299-924c-bf537131c61a/image.png)

똑똑하다... (짝짝짝)


### 로그인 구현하기

이제 그럼 과제의 중요한 부분인 로그인으로 돌아가서 설명을 하자면,

![](https://velog.velcdn.com/images/bokdol11859/post/e5aa5704-fccd-406c-aac0-50f4a69627f0/image.png)

username과 password를 보냈을 때, 그 두 값을 이용해서 authenticate함수를 실행한다. 

![](https://velog.velcdn.com/images/bokdol11859/post/773f3232-6787-4c6c-930e-3c43483d28eb/image.png)

authenticate 함수는 내가 만든게 아닌데, 저기 설명에 적힌것처럼 주어진 데이터의 유저가 존재하면 그 유저를 반환하는 함수이다. 

그래서 만약 유저가 존재한다면? 그 유저의 토큰값을 찾아와서 반환을 하고, 만약 존재하지 않는다면 존재하지 않는 사용자라는 메시지를 반환을 한다.

![](https://velog.velcdn.com/images/bokdol11859/post/336cd896-3745-4502-bc90-ec9e89ad5b51/image.png)

뷰는 이렇게... 생겼다.... 진짜 별거 없어요


### 로그인 테스트! ! !

아까 만든 세오스 계정이 과연 제대로 로그인이 될까? 그게 너무 궁금해서 바로 테스트를 해보았습니다

![](https://velog.velcdn.com/images/bokdol11859/post/b55ab18e-e3ed-44a3-bd54-02b1f082ea67/image.png)

짜잔





## 과제 회고

---

사실 진짜 마음같아선 Refresh Token 구현과 로그아웃 구현도 하고 싶었지만,,, 하필은 쿠팡 코테가 과제 제출 날짜와 겹치는 바람에. . .. 쿠팡한테 호되게 혼나고 와서 멘탈이 조금 아픈 상태입니다.. ~~개발자가 맞는 진로인지 진지하게 고민중~~


아무튼 회원가입이랑 로그인을 구현을 해봤는데, 좀 어려웠다.. 정보가 많은데 뭔가 올라온 정보들을 이해하는데에 필요한 사전 지식들이 좀 있는 것 같다.. 블로그 글을 쓰신 분들은 다 그 사전 지식이 있으셔서 그런지 그냥 금방 금방 넘기는데, 이제 그 지식이 없는 나는.... 왜 자꾸 글이 널뛰기를 하나 싶다

책을 통해서 공부를 좋아하는 나는 결국 이전에 보던 DRF 책을 다시 꺼내서 읽으면서 과제를 했다.. 벌써 서비스 개발 시작하는게 두렵다... 그래도.. 재밌다.. ~~재밌나..?~~

처음 시작했을 떄 아무것도 없던 내 투두메이트 클론이 이제는 회원가입도, 로그인도, 이것저것 생성도 가능한 나름 완성도가 있는 클론이 되어가기 시작했다. 벌써 정들었따

다음 과제도 열심히 하겠습니다... 감사합니다

