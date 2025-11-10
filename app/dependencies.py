from typing import AsyncGenerator  # Добавляем импорт
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

async def provide_session() -> AsyncGenerator[AsyncSession, None]:  # Правильный тип
    """Provide database session dependency"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def provide_user_service() -> UserService:
    """Provide user service dependency"""
    user_repository = UserRepository()
    return UserService(user_repository)
