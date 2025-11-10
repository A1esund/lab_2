import os
from typing import AsyncGenerator  # Добавляем импорт
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.models import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://user:password@localhost:5432/mydatabase"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:  # Правильный тип
    """Асинхронный генератор для предоставления сессии БД"""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def create_tables():
    """Создание таблиц в БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
