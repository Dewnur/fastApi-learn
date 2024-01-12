import asyncio
import json

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.core.config import get_settings
from app.db.session import engine, async_session
from app.main import app
from app.models import Base, Role, User, Profile, Category, Product

settings = get_settings()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.mode == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"mocks/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    roles = open_mock_json("roles")
    users = open_mock_json("users")
    profiles = open_mock_json("profiles")
    categories = open_mock_json("categories")
    products = open_mock_json("products")

    async with async_session() as session:
        for Model, values in [
            (Role, roles),
            (User, users),
            (Profile, profiles),
            (Category, categories),
            (Product, products),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """
    Создает экземпляр цикла событий по умолчанию для каждого тестового случая.
    Тесты не работают без этой функции!
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    "Асинхронный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def auth_user_ac():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/api/v1/auth/login", json={
            "email": "user@test.com",
            "password": "root",
        })
        assert ac.cookies["market_access_token"]
        yield ac


@pytest.fixture(scope="session")
async def auth_admin_ac():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/api/v1/auth/login", json={
            "email": "admin@test.com",
            "password": "root",
        })
        assert ac.cookies["market_access_token"]
        yield ac


@pytest.fixture(scope="session")
async def get_db_session():
    async with async_session() as session:
        yield session
