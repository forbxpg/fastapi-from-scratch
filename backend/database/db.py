from typing import Generator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

import settings


engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> Generator:
    """Получает объект сессии БД."""
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()
