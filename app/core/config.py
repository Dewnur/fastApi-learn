from functools import lru_cache
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    mode: Literal['DEV', 'TEST', 'PROD']
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    FILE_SAVE_DIR: str = '../data/hash/'

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_name: str
    postgres_db: str

    @property
    def postgres_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    test_postgres_host: str
    test_postgres_port: int
    test_postgres_user: str
    test_postgres_password: str
    test_postgres_name: str
    test_postgres_db: str

    @property
    def test_postgres_url(self):
        return f"postgresql+asyncpg://{self.test_postgres_user}:{self.test_postgres_password}@{self.test_postgres_host}:{self.test_postgres_port}/{self.test_postgres_db}"

    encrypt_key: str
    access_token_expire_minutes: int
    name_access_token: str = 'market_access_token'


@lru_cache()
def get_settings():
    return Settings()
