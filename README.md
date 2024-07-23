# fitsFileRenderingServer
### 김윤하 창개연 도와주기

---

Svelte 개발환경
===
```commandline
> npm create vite@latest frontend -- --template svelte
> cd frontend
frontend> npm install
frontend> npm run dev
```

---
Uvicorn(서버) 환경 설정
===
```commandline
> pip install "uvicorn[standard]"
> uvicorn main:app --reload
```

---
Alembic(Database) 환경 설정, revision 파일 생성
===
```commandline
> pip install alembic
> alembic init -t async migrations
> alembic revision --autogenerate -m [message]
> alembic upgrade head
```