from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

import nest_asyncio
from pyngrok import ngrok, conf
from uvicorn import run as uvicornRun

from domain.photo import photo_router

# import models
# from database import async_engine
# models.Base.metadata.create_all(bind=async_engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(photo_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))


@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")


if __name__ == "__main__":
    conf.get_default().auth_token = '2jba7lixTTJ2tkjm2xdDEtUEl6n_2BYTQy2fQ2ab5NBwWzPhU'
    conf.get_default().region = 'jp'
    ngrok_tunnel = ngrok.connect(8000)
    tunnels = ngrok.get_tunnels()
    for kk in tunnels:
        print(kk)
    nest_asyncio.apply()
    uvicornRun("main:app", port=8000, reload=True)
