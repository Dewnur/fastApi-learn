from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from sqlalchemy import NullPool, QueuePool
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import get_settings
from app.pages.client import client_router

settings = get_settings()

app = FastAPI()

app.mount(
    path="/static",
    app=StaticFiles(directory=settings.static_files_dir),
    name="static"
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=get_settings().postgres_url,
    engine_args={
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
        "poolclass": NullPool
        if get_settings().mode == 'TEST'
        else QueuePool,
    },
)

app.include_router(client_router, prefix='/pages', tags=['pages'])
app.include_router(api_router, prefix=get_settings().API_V1_STR)
