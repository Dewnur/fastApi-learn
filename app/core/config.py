from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_name: str
    postgres_db: str

    postgres_url: PostgresDsn | None = None

    @field_validator('postgres_url')
    @classmethod
    def get_postgres_url(cls, v, info: FieldValidationInfo) -> Any:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data['postgres_user'],
            password=info.data['postgres_password'],
            host=info.data['postgres_host'],
            port=info.data['postgres_port'],
            path=f"/{info.data['postgres_db'] or ''}",
        )


@lru_cache()
def get_settings():
    return Settings()
