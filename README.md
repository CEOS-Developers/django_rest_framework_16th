# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포


## 2주차 미션: DB 모델링 및 Django ORM



### 투두메이트 모델링 ERD
<img width="100%" src="https://user-images.githubusercontent.com/69039161/193574215-f5b00be6-6c1d-4c31-93b2-5fba237251a9.png"/>  
사용자 : 프로필 = 1 : 1  

사용자 : 팔로잉 = N : M  

사용자 : 목표 = 1 : N  

사용자 : 일기 = 1 : N  

사용자 : 시간 알림 = 1 : N  

프로필 : 팔로잉 = 1 : 

목표 : 할 일 = 1 : N  

목표 : 간편입력 = 1 : N  

목표 : 보관함 = 1 : N  

간편입력 : 요일 = N : M  

간편입력 : 할 일 = 1 : N  

할 일 : 할 일 응원 : 사용자 = 1 : 1 : 1  

일기 : 일기 응원 : 사용자 = 1 : 1 : 1  



<img width="70%" src="https://user-images.githubusercontent.com/69039161/193409903-e5bf1a4d-c8c1-4f78-9b5e-07da2b214dea.png"/>

<img width="70%" src="https://user-images.githubusercontent.com/69039161/193410055-a452a0d0-ee5d-419d-a6ba-8065aaf64ba2.png"/>
<img width="70%" src="https://user-images.githubusercontent.com/69039161/193410082-e9023040-9cf4-4491-9511-4caa5f0fb7ac.png"/>

<img width="70%" src="https://user-images.githubusercontent.com/69039161/193410103-71233aaf-786b-49fd-be7d-d8f9539c2ed8.png"/>

<img width="70%" src="https://user-images.githubusercontent.com/69039161/193410124-0a94e05a-ff60-462d-a67d-c85961bafe21.png"/>


### ORM 활용해보기
1. **데이터베이스에 해당 모델 객체 3개 넣기**
	![image](https://user-images.githubusercontent.com/69039161/193408634-cabb82c2-fe0a-4a78-9080-203e778f3e70.png)  
	
2. **삽입한 객체들을 쿼리셋으로 조회해보기 (단, 객체들이 객체의 특성을 나타내는 구분가능한 이름으로 보여야 함)**

	![스크린샷(177)](https://user-images.githubusercontent.com/69039161/193408735-5cb78a3d-60fb-4590-8496-465e559f10f1.png)  
    
3. **filter 함수 사용해보기**
	![image](https://user-images.githubusercontent.com/69039161/193408722-b9e9f262-edcc-409a-a184-8406d015dd6b.png)  


### 간단한 회고

#### 1. null=True와 blank=True
null=True와 blank=True의 차이
null=True 는 필드의 값이 NULL(정보 없음)로 저장되는 것을 허용합니다. 결국 데이터베이스 열에 관한 설정입니다.  
blank=True 는 필드가 폼(입력 양식)에서 빈 채로 저장되는 것을 허용합니다. 장고 관리자(admin) 및 직접 정의한 폼에도 반영됩니다.  
null=True 와 blank=True 를 모두 지정하면 어떤 조건으로든 값을 비워둘 수 있음을 의미합니다.  
단, CharFields()와 TextFields()에서는 예외입니다.
장고는 이 경우 NULL을 저장하지 않으며, 빈 값을 빈 문자열('')로 저장합니다.

#### 2. 어려웠던 부분

1. 간편 입력으로 입력된 할 일을 활성화하면 간편 입력과 수정, 삭제가 동기화되지 않는다.  
그런데 다시 보관함으로 이동하면 간편입력과 동기화돼서, 간편 입력을 통해 수정과 삭제가 된다.  
활성화한 일의 시간을 바꾸고 다시 보관함으로 이동해 비활성화시키면 입력했던 시간은 사라진다. 
간편 입력과 할 일의 관계가 어떻게 된건지 아직도 모르겠다. 일단은 on_delete=CASCADE라고 썼고 수정, 삭제할 때 is_active가 true인 할 일은 수정하지 않는다라고 생각하기로 했고, 삭제를 할 때는 is_active가 true인 할 일의 foreignkey를 없애고 삭제한다는 말도 안되는 기능을 가정하기로 했다~!


2. 팔로우/팔로잉 기능도 어떻게 짜야할지 고민하다가 그냥 프로필에 manytomanyfield로 넣었고, user에서는 follower라는 단어로 가져온다고 가정했는데 더 좋은 방법이 있을 것 같다. 

3. 할 일과 일기를 응원하는 기능은 manytomanyfield로 연결하려고 했지만 응원마다 이모지가 반드시 있어야 해서 각각 두 개의 외래키로 연결된 모델 클래스를 만들었다. 

4. 간편입력에서 반복되는 요일은 선택하는 부분도 고민이 됐다. 여러 요일을 선택하지만 선택지가 7개밖에 없는데 manytomanyfield를 사용하는게 이상하다는 생각이 들었다. 그런데 choicefield에서 여러 개를 선택하려면 django-multiselectfieldf를 설치해야한다는 stackoverflow를 보고 그냥 했다. 

5. erd를 짜고 나니 날짜로 필터링되는 경우가 훨씬 많을 것 같아서 좀 더 날짜 중심으로 erd를 짜는게 더 좋을 것 같다는 생각이 들었지만 시간이 없었다. 

투두메이트에 기능이 이렇게 많은지 몰랐다. 생각보다 오래걸렸다ㅜ 모델이 도대체 어떻게 짜여진건지 모르겠는 기능들이 있어서 고민을 많이 해야 했다. 특히 간편 입력 기능이 너무 어려웠다. 할 일이 활성화됐다가 간편 입력이었다가 보관함에 가는 기준을 알려고 투두메이트를 만들어보고 모르는 사람 팔로우도 했다! 





## 3주차 미션: Serializer

### 1.데이터 삽입
![image](https://user-images.githubusercontent.com/69039161/194701450-30025ff8-aaf6-450b-a7f2-dd0556a6c0d5.png)


### 2. 모든 데이터를 가져오는 API 만들기
![image](https://user-images.githubusercontent.com/69039161/194701624-0ddbe8ef-e22d-403e-a5ae-6cf8ec6ac083.png)  


### 3. 특정 데이터를 가져오는 API 만들기
![image](https://user-images.githubusercontent.com/69039161/194701692-c45a3d86-3c34-4f0c-a385-4721487c85ce.png)

### 4. 새로운 데이터를 create하도록 요청하는 API 만들기
![image](https://user-images.githubusercontent.com/69039161/194701796-8c8357f4-1501-4675-9ead-a9030dbcaf9b.png)

### 5. 특정 데이터를 삭제 또는 업데이트하는 API

수정하기
![image](https://user-images.githubusercontent.com/69039161/194702348-94c4f387-f5b3-44f5-9e4f-5116f6a7cf72.png)

삭제하기
![image](https://user-images.githubusercontent.com/69039161/194702448-62115c59-d914-43b1-9183-d494da1bfd6c.png)


### 간단한 회고
api view를 사용하지 않으면 Response를 사용할 수 없다는 것을 알게 되었다. 
api view에서 데이터를 가져올 때는 request.data로 바로 사용했는데 view를 통해 가져올 때는
`JSONParser().parse(request)`로 파싱해서 사용하는데 request가 json 포맷이 아닌건지 궁금했다. 내가 입력하고 요청하는 데이터들이 어떤 형태로 전달되는지 잘 알아야 할 것 같다. 

pycharm에 대해서 새롭게 알게 된 점: . [가상환경이름]/Scripts/activate 을 해도 알 수 없는 명령어라는 말만 나와서
답답했는데 파이참에서는 settings > Tools > Terminal > Activate virtualenv 가 체크되어 있으면 가상환경이 자동 실행되는데 윈도우에서는 display 오류로 (venv)가 보이지 않는다는 것을 알게 됐다.      






## 3주차 미션: Serializer
### 1. **DRF API View 의** CBV 으로 리팩토링하기
![image](https://user-images.githubusercontent.com/69039161/201476614-de6907dd-2d8b-42e2-bf54-86b8e24b5e84.png)  



### 2. Viewset으로 리팩토링하기
<image width=70% src="https://user-images.githubusercontent.com/69039161/201476662-b7e21c94-cb56-4ef7-8ac4-20e75190f9fa.png">


<image width=70% src="https://user-images.githubusercontent.com/69039161/201476688-fcd10cb4-3cad-4ecd-86a3-7f8ca3b6fcac.png">

코드 두 줄만으로 list, create view가 생긴다는게 신기했다. 

### 3. filter 기능 구현하기
<image width=70% src="https://user-images.githubusercontent.com/69039161/201477209-f57c03e6-8c50-45a0-abef-a6a7672c4319.png">
pip install django-filters를 하고, INSTALLED_APPS에 추가해야 했다. 
구체적으로 커스텀해서 필터링을 해야 할 일이 있을 때나, 필터링을 다양하게 많이 해야할 때 좋을 것 같았다.

### 새롭게 알게 된 점
viewset과 router를 사용하면 url을 따로 설정할 필요 없이 drf가 알아서 다 해준다는 걸 알게 되었다.
코드를 조금만 써도 흔한 커뮤니티 같은 것들이 만들어질 수도 있다는 것을 체감했던 것 같다. 

model을 수정했는데 migration을 해도 새로운 class와 field가 mysql db에 반영이 안되는 것 같은 오류가 생겼다.
일단 수정하지 않고 미션을 했는데 뭐가 문제인지 더 찾아봐야할 것 같다. 


## 4주차 미션: SimpleJWT

#### Q. 로그인 인증 방식은 어떤 종류가 있나요?
1. 세션과 쿠키를 통한 인증  
   사용자가 로그인을 하면 서버가 계정 정보를 확인한 후, 세션 저장소에 저장하고 연결되는 세션 ID를 발급한다. 
   서버가 HTTP 응답 헤더에 session id를 보낸다.  
   이후 클라이언트가 http 요청을 보낼 때마다 Session id가 담긴 쿠키를 http요청 헤더에 실어 보낸다.  
   -> 세션을 서버가 저장하고 있고, 서버에게 요청을 보낼 때마다 인증을 위해 세션 id를 보내는데 그 id를 담는게 쿠키다. 
2. Access Token을 이용한 인증  
   Header, Payload, Verify Signature 객체를 필요로 한다. payload는 만료일시, 발급자, 발급 일시 등 토큰에 담을 정보를 포함한다. 
   verify signature는 payload가 위변조되지 않았다는 것을 증명하는 문자열이다. 
   Base64방식으로 인코딩한 Header, payload, secret key를 서명한다. 
3. Access Token + Refresh Token을 이용한 인증  
   Access token을 오래 사용할 경우 토큰이 해커에게 탈취되는 문제를 해결한다.   
   access token이 만료되면, access와 refresh를 같이 보내며 새로운 token 발급 요청을 할 수 있다.   
   -> 사용자는 refresh 토큰이 만료될 때만 다시 로그인을 하면 되지만, access token의 유효 기간마다 토큰이 새롭게 발급 되어 안전성은 올라간다.
4. OAuth 2.0을 이용한 인증  
   이 방법에서 클라이언트=내가 만드는 앱의 서버, 서버=인증에 이용할 sns의 auth서버와 OAuth 자원 관리 서버(Google등 OAuth를 통해 접근을 지원하는 제공자)가 된다.   
   사용자가 앱에 인증 요청을 하면 인증할 수단(구글 로그인 등)을 보여주고, 사용자가 로그인 정보를 입력한다. 애플리케이션이 사용자가 인증했다는 권한 증서를 auth 서버에 보내면, auth는 앱에게 
   토큰과 유저 정보를 발급해주고 앱은 그걸 db에 저장한다. 사용자가 자원을 요청하면 앱은 OAuth자원 관리 서버에 토큰과 함께 요청을 보내고, 유효하다면 자원을 응답 받는다. 

#### Q. JWT 는 무엇인가요?
Json Web Token. 인증에 필요한 정보들을 암호화한 JSON 토큰  

`서버기반 인증`은 사용자가 많아질수록 관리가 어렵다. 하나의 서버의 성능을 높이는 것보다 여러 대의 서버를 두는 수평 확장은 경제적 부담이 적고 유연해서 일반적인 방법.
모든 서버에서 유저의 세션 id를 공유해야한다는 단점이 있다.   
`토큰 기반 인증`에서는 클라이언트가 토큰을 저장하고, 서버는 토큰 발급과 검증만 해서 서버가 저장하고 있는 것은 없다.

헤더에는 토큰 유형, 암호화 알고리즘 두 가지가 포함된다.   
페이로드는 사용자 정보와 데이터 속성을 포함하는 등록된 클레임, 공개 클레임, 비공개 클레임으로 나뉘는 클레임 단위로 구성된다.   
서명은 인코딩된 헤더, 페이로드 + secret key를 특정 암호화 알고리즘을 이용해 암호화한다. 보통 HMAC SHA256 또는 RSA가 사용된다

#### Q. JWT 로그인 구현하기 
HTTP Request
![image](https://user-images.githubusercontent.com/69039161/202851928-05ddd47e-eb28-4790-a6d0-76489551565e.png)

HTTP Response(로그인 성공)
![image](https://user-images.githubusercontent.com/69039161/202851955-c1af1edd-c757-4450-8b36-9c8f2cdf1327.png)

HTTP Response(로그인 실패)
![image](https://user-images.githubusercontent.com/69039161/202852082-01891e17-c440-49ce-94e1-8dc979bf0488.png)


### 간단한 회고
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency account.0001_initial on database 'default'.  
-> 그냥  mysql database를 삭제해버렸다. 새로운 필드를 추가할 때마다 이 오류가 생긴다. migration 파일만 삭제해도 같은 오류가 나고, 아예 db를 삭제하고 다시 만들어야 오류가 나오지 않는다. 이유가 궁금했다.

로그인을 구현할 때 대충 상황에 맞는 거 쓰면서 구현했던 것 같은데, 인증 방식 4가지에 대해 정확하게 이해할 수 있는 기회가 되었다. 

# 6주차 AWS : EC2, RDS & Docker & Github Action


ModuleNotFoundError: No module named 'rest_framework_simplejwt'  
-> requirements.txt 수정

error: command 'gcc' failed: No such file or directory  
->`sudo apt-get update`  
`sudo apt-get install gcc`
안됨


RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base \
               && apk add gcc libc-dev libffi-dev \  
               && apk add zlib-dev jpeg-dev gcc musl-dev 


pillow를 설치할 때 필요한 build dependency들이 있다고 해서 Dockerfile에 추가해야했다.
virtual로 설치하고 다시 삭제해서 image크기를 작게하는 것이 좋다고 하지만 일단 돌아가는 것을 확인하는게 급했다. 

닫으려는데 또 에러ㅜㅜ
failed to remove network django_rest_framework_16th_default: Error response from daemon: error while removing network

`docker network ls`
![image](https://user-images.githubusercontent.com/69039161/204083135-e20f4cd5-89f3-4b25-8844-acfff250868b.png)
host가 있어서 그런가?  
bridge, host, none은 Docker 데몬(daemon)이 실행되면서 디폴트로 생성되는 네트워크입니다. 대부분의 경우에는 이러한 디폴트 네트워크를 이용하는 것 보다는 사용자가 직접 네트워크를 생성해서 사용하는 것이 권장됩니다.  
라고 함. 

네트워크에 연결되어 있는 도커가 없어야 삭제할 수 있다고 하는데, 삭제 명령어가 다 안먹혀서 docker desktop으로 stop하니까 종료가 됐다. ㅠ
![image](https://user-images.githubusercontent.com/69039161/204083612-c07c32b1-64c5-4dba-960b-4b1160939f20.png)
 
--> 여기까지는 로컬에서 검사만 한 거였다. 이때까지는 정말 행복했다.

EC2, RDS를 만들고 master에 push를 했는데 또 pillow 에러가 났다.  
`RUN python -m pip install --upgrade pip`
얘도 더해줘야 했다. 위에 더한 애를 빼고 얘만 있으면 또 안된다.   
이유가 뭔지 모르겠다. alpine image? 파이썬 버젼이 달라서 그런건지.. 
ubuntu 버전이 달라서 그런건지? 저 alpine 이미지가 정확히 뭔지도 모르겠다.  

이제 400 에러가 났다. ec2 rds 문제인건가 ec2도 rds도 잘 접속되고 도커도 잘 돌아가고 있었는데
뭐지 이러면서 ec2랑 rds 다섯번은 다시 만든 것 같다. vpc, az, security group 공부를 했다. 
무지성에서 지성되기도 다섯 번은 읽은 것 같은데 아직도 나는 지성이 없다.  
정말 기억에 남을 만한 삽질이었다. 

docker-compose.prod.yml에 env_file이 example로 되어있었다. 세상에. 우리 아이한테 secret key도 알려주지 않고
 django 프로젝트를 띄우라고 강요하고 있었다. 여기서 .env는 deploy.sh에서 만든 .env인 것 같음.

![image](https://user-images.githubusercontent.com/69039161/204132282-27de2264-2b6a-4b46-a1fe-cbc2dd49beca.png)

이제 500이 뜬다. 

![image](https://user-images.githubusercontent.com/69039161/204136903-fb5bdf07-2d1c-4775-8105-0af304c60cb5.png)
아악 드디어
![image](https://user-images.githubusercontent.com/69039161/204136953-e603f2f3-82f3-4661-bfb4-8d0d11348ea6.png)
다른 분들 레포 보고 migrate 코드 추가했는데 왜 migrate가 안되지 이러고 있었는데
ec2 cli에서 todomate database를 생성하고 .env.prod 에서 이름도 수정하니까 바꾸니까 됐다. 
DB식별자를 database 이름이라고 생각하고 database-1이라고 했었는데 mysql에서 하이픈을 db이름에 넣을 수 없어서
생긴 문제인 것 같다.

