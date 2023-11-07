import asyncio
import json

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.core.config import get_settings
from app.db.session import engine, async_session
from app.main import app
from app.models import Base, Role, User

settings = get_settings()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.mode == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mocks/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    roles = open_mock_json("roles")
    users = open_mock_json("users")

    async with async_session() as session:
        for Model, values in [
            (Role, roles),
            (User, users),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each tests case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    "Асинхронный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/api/v1/auth/login", json={
            "email": "tests@tests.com",
            "password": "tests",
        })
        assert ac.cookies["market_access_token"]
        yield ac
