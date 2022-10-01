
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
