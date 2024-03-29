import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    mode: Literal['DEV', 'TEST', 'PROD']
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    FILE_SAVE_DIR: str = '../data/hash/'

    @property
    def base_dir(self):
        return Path(__file__).resolve().parents[2]

    @property
    def static_files_dir(self):
        return os.path.join(self.base_dir, 'app', 'static')

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_name: str
    postgres_db: str

    @property
    def postgres_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    encrypt_key: str
    access_token_expire_minutes: int
    name_access_token: str = 'market_access_token'


@lru_cache()
def get_settings():
    return Settings()
