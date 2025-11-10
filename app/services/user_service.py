"""Service layer for User operations.

Этот файл реализует класс `UserService`, который использует слой репозитория
(`UserRepository`) для выполнения CRUD‑операций.  
Сервис не открывает сессию сам – ей передаётся объект `AsyncSession`
от вызывающего кода (например, зависимость, предоставляющая scoped session).
"""

import uuid
from typing import List, Optional

from app.repositories.user_repository import UserRepository, UserCreate, UserUpdate
from src.models import User


class UserService:
    """Бизнес‑логика управления пользователями."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(
        self,
        session: "AsyncSession",
        user_id: uuid.UUID,
    ) -> Optional[User]:
        """
        Получить пользователя по его UUID.

        Параметры
        ----------
        session : AsyncSession
            Сессия БД для выполнения запроса.
        user_id : uuid.UUID
            Идентификатор пользователя.

        Возвращает
        ---------
        User | None
            Найдённый пользователь или ``None`` если не найден.
        """
        return await self.user_repository.get_by_id(session, user_id)

    async def get_by_filter(
        self,
        session: "AsyncSession",
        count: int,
        page: int,
        **kwargs,
    ) -> List[User]:
        """
        Получить пользователей по фильтрам с пагинацией.

        Параметры
        ----------
        session : AsyncSession
            Сессия БД для выполнения запроса.
        count : int
            Количество записей на странице.
        page : int
            Номер страницы (от 1).
        **kwargs :
            Дополнительные фильтры, передающиеся репозиторию.
            Типичные ключи: ``username`` и ``email``.

        Возвращает
        ---------
        List[User]
            Список пользователей, удовлетворяющих фильтру.
        """
        return await self.user_repository.get_by_filter(session, count, page, **kwargs)

    async def create(
        self,
        session: "AsyncSession",
        user_data: UserCreate,
    ) -> User:
        """
        Создать нового пользователя.

        Параметры
        ----------
        session : AsyncSession
            Сессия БД для выполнения операции.
        user_data : UserCreate
            DTO, содержащий поля, необходимые для создания.

        Возвращает
        ---------
        User
            Новый пользователь с заполненным UUID.
        """
        return await self.user_repository.create(session, user_data)

    async def update(
        self,
        session: "AsyncSession",
        user_id: uuid.UUID,
        user_data: UserUpdate,
    ) -> Optional[User]:
        """
        Обновить существующего пользователя.

        Параметры
        ----------
        session : AsyncSession
            Сессия БД для выполнения операции.
        user_id : uuid.UUID
            Идентификатор обновляемого пользователя.
        user_data : UserUpdate
            DTO, содержащий поля, которые нужно изменить.

        Возвращает
        ---------
        Optional[User]
            Обновлённый пользователь или ``None`` если ничего не изменено / пользователь не найден.
        """
        return await self.user_repository.update(session, user_id, user_data)

    async def delete(
        self,
        session: "AsyncSession",
        user_id: uuid.UUID,
    ) -> None:
        """
        Удалить пользователя по его UUID.

        Параметры
        ----------
        session : AsyncSession
            Сессия БД для выполнения операции.
        user_id : uuid.UUID
            Идентификатор удаляемого пользователя.
        """
        await self.user_repository.delete(session, user_id)