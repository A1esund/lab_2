import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.schemas.order import OrderCreate, OrderUpdate
from src.models import Order


class OrderService:
    """Бизнес-логика управления заказами."""

    def __init__(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository):
        self.order_repository = order_repository
        self.user_repository = user_repository
        self.product_repository = product_repository

    async def get_by_id(
        self,
        session: AsyncSession,
        order_id: uuid.UUID,
    ) -> Optional[Order]:
        """Получить заказ по его UUID."""
        return await self.order_repository.get_by_id(session, order_id)

    async def get_by_filter(
        self,
        session: AsyncSession,
        count: int,
        page: int,
        **kwargs,
    ) -> List[Order]:
        """Получить заказы по фильтрам с пагинацией."""
        return await self.order_repository.get_by_filter(session, count, page, **kwargs)

    async def create_order(
        self,
        session: AsyncSession,
        order_data: OrderCreate,
    ) -> Order:
        """Создать новый заказ."""
        # Проверяем, что пользователь существует
        user = await self.user_repository.get_by_id(session, order_data.user_id)
        if not user:
            raise ValueError(f"User with id {order_data.user_id} not found")
        
        # Проверяем, что все продукты существуют и доступны в нужном количестве
        for item in order_data.items:
            product = await self.product_repository.get_by_id(session, item.product_id)
            if not product:
                raise ValueError(f"Product with id {item.product_id} not found")
            if product.stock_quantity < item.quantity:
                raise ValueError(f"Insufficient stock for product {item.product_id}. Available: {product.stock_quantity}, Requested: {item.quantity}")
        
        # Создаем заказ
        order = await self.order_repository.create(
            session,
            user_id=order_data.user_id,
            address_id=order_data.address_id,
            items=[{"product_id": item.product_id, "quantity": item.quantity} for item in order_data.items],
            total_price=order_data.total_price,
            status=order_data.status
        )
        
        return order

    async def update(
        self,
        session: AsyncSession,
        order_id: uuid.UUID,
        order_data: OrderUpdate,
    ) -> Order:
        """Обновить существующий заказ."""
        # Собираем только те поля, которые были переданы
        update_data = {}
        if order_data.user_id is not None:
            update_data['user_id'] = order_data.user_id
        if order_data.address_id is not None:
            update_data['address_id'] = order_data.address_id
        if order_data.total_price is not None:
            update_data['total_price'] = order_data.total_price
        if order_data.status is not None:
            update_data['status'] = order_data.status
        
        order = await self.order_repository.update(session, order_id, **update_data)
        if not order:
            raise ValueError(f"Order with id {order_id} not found")
        return order

    async def delete(
        self,
        session: AsyncSession,
        order_id: uuid.UUID,
    ) -> bool:
        """Удалить заказ по его UUID."""
        return await self.order_repository.delete(session, order_id)