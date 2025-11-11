import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.params import Parameter

from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserCreate, UserUpdate


class UserController(Controller):
    path = "/users"

    @get("/{user_id:uuid}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        db_session: AsyncSession,
        user_id: uuid.UUID = Parameter(),
    ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(db_session, user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get("/")
    async def get_all_users(
        self,
        user_service: UserService,
        db_session: AsyncSession,
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
            
        users = await user_service.get_by_filter(db_session, count, page, **filters)
        return [UserResponse.model_validate(user) for user in users]

    @post("/")
    async def create_user(
        self,
        user_service: UserService,
        db_session: AsyncSession,
        user_data: UserCreate,
    ) -> UserResponse:
        """Создать нового пользователя"""
        # user_create_dto = UserCreate(
        #     username=user_data.username,
        #     email=user_data.email
        # )
        
        user = await user_service.create(db_session, user_data)
        await db_session.commit()
        return UserResponse.model_validate(user)

    @delete("/{user_id:uuid}")
    async def delete_user(
        self,
        user_service: UserService,
        db_session: AsyncSession,
        user_id: uuid.UUID = Parameter(),
    ) -> None:
        """Удалить пользователя"""
        deleted = await user_service.delete(db_session, user_id)
        if not deleted:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        await db_session.commit()

    @put("/{user_id:uuid}")
    async def update_user(
        self,
        user_service: UserService,
        db_session: AsyncSession,
        user_data: UserUpdate,
        user_id: uuid.UUID = Parameter(),
    ) -> UserResponse:
        """Обновить пользователя"""
        # user_update_dto = UserUpdate(
        #     username=user_data.username,
        #     email=user_data.email
        # )
        
        user = await user_service.update(db_session, user_id, user_data)
        await db_session.commit()
        return UserResponse.model_validate(user)
