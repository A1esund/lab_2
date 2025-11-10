import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.params import Parameter

from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.repositories.user_repository import UserCreate as UserCreateRepo, UserUpdate as UserUpdateRepo
from app.dependencies import provide_session


class UserController(Controller):
    path = "/users"
    dependencies = {
        "user_service": Provide("user_service"),
        "session": Provide(provide_session)
    }

    @get("/{user_id:uuid}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        session: AsyncSession,
        user_id: uuid.UUID = Parameter(),
    ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(session, user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get("/")
    async def get_all_users(
        self,
        user_service: UserService,
        session: AsyncSession,
        count: int = Parameter(gt=0, le=100, default=10),
        page: int = Parameter(ge=1, default=1),
        username: str = Parameter(default=""),
        email: str = Parameter(default=""),
    ) -> List[UserResponse]:
        """Получить всех пользователей с пагинацией и фильтрацией"""
        filters = {}
        if username:
            filters["username"] = username
        if email:
            filters["email"] = email
            
        users = await user_service.get_by_filter(session, count, page, **filters)
        return [UserResponse.model_validate(user) for user in users]

    @post("/")
    async def create_user(
        self,
        user_service: UserService,
        session: AsyncSession,
        user_data: UserCreate,
    ) -> UserResponse:
        """Создать нового пользователя"""
        user_create_dto = UserCreateRepo(
            username=user_data.username,
            email=user_data.email
        )
        
        user = await user_service.create(session, user_create_dto)
        await session.commit()
        return UserResponse.model_validate(user)

    @delete("/{user_id:uuid}")
    async def delete_user(
        self,
        user_service: UserService,
        session: AsyncSession,
        user_id: uuid.UUID = Parameter(),
    ) -> None:
        """Удалить пользователя"""
        deleted = await user_service.delete(session, user_id)
        if not deleted:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        await session.commit()

    @put("/{user_id:uuid}")
    async def update_user(
        self,
        user_service: UserService,
        session: AsyncSession,
        user_data: UserUpdate,
        user_id: uuid.UUID = Parameter(),
    ) -> UserResponse:
        """Обновить пользователя"""
        user_update_dto = UserUpdateRepo(
            username=user_data.username,
            email=user_data.email
        )
        
        user = await user_service.update(session, user_id, user_update_dto)
        await session.commit()
        return UserResponse.model_validate(user)
