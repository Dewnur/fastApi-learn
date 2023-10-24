from fastapi import FastAPI
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware

from app.api.v1.api import api_router
from app.core.config import get_settings

app = FastAPI()

app.include_router(api_router)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=get_settings().postgres_url,
    engine_args={              # engine arguments example
        "echo": False,          # print all SQL statements
        "pool_pre_ping": True, # feature will normally emit SQL equivalent to “SELECT 1” each time a connection is checked out from the pool
        "pool_size": 5,        # number of connections to keep open at a time
        "max_overflow": 10,    # number of connections to allow to be opened above pool_size
    },
)