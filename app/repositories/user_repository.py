import uuid
from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User


class UserCreate:
    """Схема для создания пользователя"""
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email


class UserUpdate:
    """Схема для обновления пользователя"""
    def __init__(self, username: Optional[str] = None, email: Optional[str] = None):
        self.username = username
        self.email = email


class UserRepository:
    """Репозиторий для работы с пользователями"""
    
    async def get_by_id(self, session: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        """Получить пользователя по ID"""
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_filter(self, session: AsyncSession, count: int, page: int, **kwargs) -> List[User]:
        """Получить пользователей по фильтрам с пагинацией"""
        stmt = select(User)
        
        # Применяем фильтры
        if 'username' in kwargs and kwargs['username']:
            stmt = stmt.where(User.username.ilike(f"%{kwargs['username']}%"))
        if 'email' in kwargs and kwargs['email']:
            stmt = stmt.where(User.email.ilike(f"%{kwargs['email']}%"))
        
        # Применяем пагинацию
        offset = (page - 1) * count
        stmt = stmt.offset(offset).limit(count)
        
        result = await session.execute(stmt)
        return result.scalars().all()
    
    async def create(self, session: AsyncSession, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        user = User(
            username=user_data.username,
            email=user_data.email
        )
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return user
    
    async def update(self, session: AsyncSession, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        """Обновить пользователя"""
        # Собираем только те поля, которые были переданы
        update_data = {}
        if user_data.username is not None:
            update_data['username'] = user_data.username
        if user_data.email is not None:
            update_data['email'] = user_data.email
        
        if not update_data:
            # Если нет данных для обновления, возвращаем пользователя без изменений
            user = await self.get_by_id(session, user_id)
            if not user:
                raise ValueError(f"User with id {user_id} not found")
            return user
        
        stmt = update(User).where(User.id == user_id).values(**update_data)
        await session.execute(stmt)
        
        # Получаем обновленного пользователя
        user = await self.get_by_id(session, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user
    
    async def delete(self, session: AsyncSession, user_id: uuid.UUID) -> bool:
        """Удалить пользователя"""
        user = await self.get_by_id(session, user_id)
        if not user:
            return False
            
        stmt = delete(User).where(User.id == user_id)
        await session.execute(stmt)
        return True
