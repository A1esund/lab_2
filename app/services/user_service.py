import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession  # Добавляем импорт

from app.repositories.user_repository import UserRepository, UserCreate, UserUpdate
from src.models import User


class UserService:
    """Бизнес‑логика управления пользователями."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(
        self,
        session: AsyncSession,  # Теперь тип определен
        user_id: uuid.UUID,
    ) -> Optional[User]:
        """Получить пользователя по его UUID."""
        return await self.user_repository.get_by_id(session, user_id)

    async def get_by_filter(
        self,
        session: AsyncSession,  # Теперь тип определен
        count: int,
        page: int,
        **kwargs,
    ) -> List[User]:
        """Получить пользователей по фильтрам с пагинацией."""
        return await self.user_repository.get_by_filter(session, count, page, **kwargs)

    async def create(
        self,
        session: AsyncSession,  # Теперь тип определен
        user_data: UserCreate,
    ) -> User:
        """Создать нового пользователя."""
        return await self.user_repository.create(session, user_data)

    async def update(
        self,
        session: AsyncSession,  # Теперь тип определен
        user_id: uuid.UUID,
        user_data: UserUpdate,
    ) -> User:
        """Обновить существующего пользователя."""
        user = await self.user_repository.update(session, user_id, user_data)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user

    async def delete(
        self,
        session: AsyncSession,  # Теперь тип определен
        user_id: uuid.UUID,
    ) -> bool:
        """Удалить пользователя по его UUID."""
        return await self.user_repository.delete(session, user_id)
