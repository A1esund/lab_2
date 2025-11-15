import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from litestar import Litestar
from litestar.di import Provide

from app.controllers.user_controller import UserController
from app.controllers.product_controller import ProductController
from app.controllers.order_controller import OrderController
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService

# Настройка базы данных - используем существующий data.db
DATABASE_URL = "sqlite+aiosqlite:///./data.db"  # Путь относительно текущей директории

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}  # Важно для SQLite
)
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Провайдер сессии базы данных"""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

async def provide_user_repository() -> UserRepository:
    """Провайдер репозитория пользователей"""
    return UserRepository()

async def provide_user_service(user_repository: UserRepository) -> UserService:
    """Провайдер сервиса пользователей"""
    return UserService(user_repository)

async def provide_product_repository() -> ProductRepository:
    """Провайдер репозитория продуктов"""
    return ProductRepository()

async def provide_product_service(product_repository: ProductRepository) -> ProductService:
    """Провайдер сервиса продуктов"""
    return ProductService(product_repository)

async def provide_order_repository() -> OrderRepository:
    """Провайдер репозитория заказов"""
    return OrderRepository()

async def provide_order_service(
    order_repository: OrderRepository,
    user_repository: UserRepository,
    product_repository: ProductRepository
) -> OrderService:
    """Провайдер сервиса заказов"""
    return OrderService(order_repository, user_repository, product_repository)

app = Litestar(
    route_handlers=[UserController, ProductController, OrderController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
        "product_repository": Provide(provide_product_repository),
        "product_service": Provide(provide_product_service),
        "order_repository": Provide(provide_order_repository),
        "order_service": Provide(provide_order_service),
    },
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)


