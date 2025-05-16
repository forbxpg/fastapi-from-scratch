import asyncio
import os
from typing import Generator, Any


import asyncpg
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from starlette.testclient import TestClient

from api.v1 import schemas, routes
from database.db import get_session
import settings
from database.models import Base


TABLES_FOR_CLEAN = ("users",)


test_engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
)

test_async_session = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest.fixture(scope="session")
def get_event_loop():
    """Фикстура для получения цикла событий."""

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations() -> None:
    """Run migrations before tests."""
    os.system("alembic upgrade head")


@pytest.fixture(scope="session")
async def async_session_test():
    """Фикстура для тестовой сессии БД.

    Создает сессию для очистки таблиц.
    """
    engine = create_async_engine(
        settings.TEST_DATABASE_URL, echo=settings.DATABASE_ECHO, future=True
    )
    async_session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    yield async_session


@pytest.fixture(scope="function")
async def clean_tables(async_session_test: AsyncSession):
    """Фикстура для очистки таблиц БД.

    Очищает таблицы перед каждым тестом.
    """
    async with async_session_test() as session:
        async with session.begin():
            for table in TABLES_FOR_CLEAN:
                await session.execute(f"TRUNCATE TABLE {table} CASCADE;")


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """Фикстура для тестового клиента FastAPI.

    Создает тестовый клиент для API.
    """
    from main import app

    async def _get_test_session():
        """Создает тестовую сессию БД."""
        try:
            async with test_async_session() as session:
                yield session
        finally:
            ...

    app.dependency_overrides[get_session] = _get_test_session
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        settings.TEST_DATABASE_URL.replace("postgresql+asyncpg", "postgresql"),
    )
    yield pool
    await pool.close()


@pytest.fixture
async def get_user_from_db(asyncpg_pool):
    async def get_user_via_uuid(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                "SELECT * FROM users WHERE user_id = $1", user_id
            )

    return get_user_via_uuid
