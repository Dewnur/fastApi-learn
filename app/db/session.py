from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import get_settings

settings = get_settings()

DATABASE_PARAMS = {}
DATABASE_URL = settings.postgres_url

if settings.mode == 'TEST':
    DATABASE_PARAMS.update({'poolclass': NullPool})

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session = async_sessionmaker(engine, expire_on_commit=False)
