# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포


## 2주차 미션: DB 모델링 및 Django ORM

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
