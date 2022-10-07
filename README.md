

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

