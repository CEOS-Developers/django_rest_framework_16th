# CEOS 16기 백엔드 스터디 모델링 및 drf 연습을 위한 레포


## 2주차 미션: DB 모델링 및 Django ORM

### 투두메이트
일정 관리(투두리스트) 서비스.  
다른 사용자들에게 자신의 투두리스트를 공유할 수 있다는 차별점이 있다.  
서로 좋아요 등을 남길 수도 있고, 그래서 더 동기부여가 된다!

### 모델 설계

#### User
django에서 기본 제공하는 user 모델 상속  - AbstractUser를 상속받아 custom함
- email을 유저네임으로 사용하도록 custom

#### Follower
- follower: User를 참조하는 foreign key
- following: User를 참조하는 foreign key

#### Category
- category_name: 카테고리명
- user : User를 참조하는 foreign key, 어떤 사용자의 카테고리인지 보여줌

#### Todo
- todo_name: to do item을 작성했을 때 그것의 이름
- user: 작성한 사용자
- category: 카테고리
- disclosure_choice: 친구들에게 공개할 것인지 여부, private(비공개), only friends(친구 공개), public(전체 공개) 중 선택할 수 있도록 한다.  
default는 public(전체공개)
- date: 일정별 to do list를 볼 수 있도록

#### Comment
- todo: Todo를 참조하는 foreign key, 어떤 to do item에 대한 활동인지 보여줌
- author: User를 참조하는 foreign key, 이모티콘이나 댓글을 다는 작성자
- emoji: 한 글자짜리 이모티콘으로 반응
- comment: 서로 댓글을 달 수도 있다.

### ORM 이용해보기
1번  
![img.png](images/img.png)
2번  
![img_1.png](images/img_1.png)
3번  
![img_2.png](images/img_2.png)


### 이번 과제를 하며...
내 컴퓨터 환경에서는 pip install mysqlclient로 mysqlclient가 설치되지 않는다..  
그래서 지난번 프로젝트 때는 파이썬 버젼에 맞는 whl 파일을 인터넷에서 다운로드 받는 형식으로 이용을 했는데
다른 방법이 없나 알아봤지만 결국 이번에도 수동설치를 하게 되었다.  

또, mysql 데이터베이스를 그대로 이용할 수 없다.  
python manage.py migrate를 하면 다음 에러가 뜬다.  
![img_3.png](images/img_3.png)
이 에러를 해결하려고 시간을 엄청나게 많이 썼는데..! 답은 pip install PyMySQL을 하는 것이었다.  
다음에는 잊지 말아야지..

드디어 데이터베이스를 연결하고 모델링을 하는데, 생각보다 복잡했다!  
투두메이트는 들어보기만 하고 사용해본 적은 없는데, 그냥 투두리스트가 아니라
사용자 간 소통하는 기능이 있어서 생각할 것이 많았다. 사실 실제 앱처럼 하려면 이것보다 훨씬
복잡하고 꼼꼼하게 해야할 것 같은데, 이번 과제에서 그렇게까지 하지는 못해서 아쉽다.  

그리고 Django에서 기본적으로 제공하는 user 모델에 대해서 잘 몰랐는데, 엄청 편리한 기능 같아서
더 알아보고 싶다.


## 3주차 미션: Django Serializer & Django View

### 데이터 삽입

User 데이터 삽입
```python
class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
```
![img_4.png](images/img_4.png)

Category 데이터 삽입
```python
class Category(models.Model):
    category_name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.category_name
```
![img_5.png](images/img_5.png)

Todo 데이터 삽입
```python
class Todo(models.Model):
    DISCLOSURE_CHOICES = {
        ('private', 'Private'),
        ('onlyFriends', 'Only Friends'),
        ('public', 'Public'),
    }
    todo_name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    disclosure_choice = models.CharField(default='public', max_length=30, choices=DISCLOSURE_CHOICES)
    date = models.DateTimeField(default=now)
    def __str__(self):
        return self.todo_name
```
![img_6.png](images/img_6.png)

### API 만들기
모든 데이터를 가져오는 api
![img_7.png](images/img_7.png)

특정 과제를 가져오는 api
![img_8.png](images/img_8.png)

새로운 데이터를 create하도록 요청하는 api
![img_9.png](images/img_9.png)

특정 데이터를 삭제하는 api
![img_10.png](images/img_10.png)
![img_11.png](images/img_11.png)

특정 데이터를 업데이트하는 api
![img_12.png](images/img_12.png)
![img_13.png](images/img_13.png)


### 이번 과제를 하며...
모델들에 대해 ModelSerializer을 이용해 serializer를 만들었고,
가장 핵심 모델이라고 생각한 todo 모델에 대해 view 만들기 연습을 해봤다.

views.py를 작성할 때 처음에 과제 예시로 나온 코드를 그대로 따라했더니 오류가 났는데 해결 과정에서
JsonResponse 대신 그냥 Response를 사용해야 drf를 테스트 할 수 있는 브라우저 화면을 볼 수 있다는 사실을 알게 되었고,  
함수형 뷰를 작성할 때는 @api_view를 꼭 달아야한다는 사실도 알게 되었다.

나중에 서비스에 필요한 나머지 api들도 만들어보고 Postman도 한번 사용해 봐야겠다!