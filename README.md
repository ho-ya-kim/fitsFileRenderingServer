# fitsFileRenderingServer

---

Svelte 개발환경
===
```commandline
> npm create vite@latest frontend -- --template svelte
> cd frontend
frontend> npm install
frontend> npm run dev
```
## 만약 Frontend 개발이 끝났다면?
```commandline
frontend> npm run build
```
1. 이 방식을 통해 js, css 파일이 만들어지면 이제 Svelte의 도움을 받지 않고 `localhost:port`로 접속해서 확인할 수 있다.
2. 아래 Uvicorn에서 `--reload`를 사용했기 때문에, Frontend를 수정 하며 빌드하면서 실시간으로 수정사항을 확인할 수 있다.  


---
Uvicorn(서버) 환경 설정
===
```commandline
> pip install "uvicorn[standard]"
> uvicorn main:app --reload
```
`--reload`는 실시간으로 수정사항을 반영한다는 뜻이다.

---
Alembic(Database) 환경 설정, revision 파일 생성
===
```commandline
> pip install alembic
> alembic init -t async alembic
> alembic revision --autogenerate -m [message]
> alembic upgrade head
```
1. 이후 데이터베이스를 초기화할 때는, `alembic downgrade head` 와 `alembic upgrade head`를 실행하면 된다.
2. DB의 구조가 바꼈다면, `alembic revision --autogenerate -m [message]`를 실행해서 __revision file__을 만들고, 다시 `alembic upgrade head`를 실행하면 된다.


---
Port 관리(닫기)
===
```commandline
frontend> npm install kill-port
frontend> npx kill-port [port]
```
1. 갑자기 서버가 잘 열리지 않는다면 포트가 제대로 닫히지 않았을 가능성을 의심하자.
2. 사용하던 `port`번호로 `npx kill-port [port]`를 실행하면 된다.