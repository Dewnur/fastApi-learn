from fastapi import FastAPI
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware

from app.api.v1.api import api_router
from app.core.config import get_settings

app = FastAPI()

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=get_settings().postgres_url,
    engine_args={
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
    },
)

app.include_router(api_router, prefix=get_settings().API_V1_STR)
