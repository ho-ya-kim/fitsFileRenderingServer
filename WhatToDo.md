가상환경 설정
===
전체 작업은 가상환경에서 진행해야 한다. 가상환경을 편하게 설정하기 위해서 Jetbrain Pycharm을 이용하자.

---
Database 설정
===
## 1. Alembic 초기화
```commandline
> alembic init -t async alembic
```

## 2. alembic.ini 파일 수정

`mysql+aiomysql://{계정}:{비밀번호}@{주소}:{포트}/{database 이름}` 형식으로 수정하는것이고, 본인에게 맞게 바꾸면 된다.<br>
기본 설정을 바꾸지 않았다면`{주소}:{포트}=127.0.0.1:3306`이다.
```ini
# ./alembic.ini
...
sqlalchemy.url = mysql+aiomysql://root:dlQmstjgh1!^^@127.0.0.1:3306/fits
...
```

## 3. alembic/env.py 파일 수정
```python
# ./alembic/env.py
# 생략...
import models
# 생략...
target_metadata = models.Base.metadata
# 생략...
```

## 4. Alembic revision
```commandline
> alembic revision --autogenerate -m 1 
```
`./alembic`폴더와 내부 파일을 만든다

## 5. alembic upgrade
```commandline
> alembic upgrade head
```
데이터베이스 구성이 끝났다.

---
서버 실행
===
## 6. 서버 실행
local 서버를 테스트 하고 싶다면 다음을 실행한다.
```commandline
> uvicorn main:app --reload
```
nrgok를 이용해 public 서버를 배포 하고 싶다면 `./main.py`를 실행한다.


---
Frontend 빌드
===
## 7. 환경변수 설정
6번에서 local 이라면 `http://localhost:8000`을, public 이라면 터미널에 출력된 주소를 복사하고, `./frontend/.env`파일을 수정한다. 기존에 있는 `VITE_SERVER_URL=` 뒤에 붙이면 된다.
* Local : `VITE_SERVER_URL=https://localhost:8000`
* Public (다음은 한 가지 예시이다.) : `VITE_SERVER_URL=https://82e0-221-141-4-184.ngrok-free.app`
## 8. 빌드
```commandline
> cd frontend
frontend> npm run build
```
이 과정은 프론트엔드를 수정하고 진행하면 실시간으로 반영된다. `./frontend/.env` 파일을 이용해 데이터베이스에 연결하기 때문에 다시 빌드해 준 것이다. 

---