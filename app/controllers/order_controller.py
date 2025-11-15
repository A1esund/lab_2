from typing import List
from uuid import UUID
from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.params import Parameter
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.services.order_service import OrderService


class OrderController(Controller):
    path = "/orders"
    
    def __init__(self):
        self.dependencies = {
            "order_service": Provide(lambda: OrderService()),
        }

    @get("/")
    async def get_all_orders(
        self,
        order_service: OrderService,
        db_session: AsyncSession,
        count: int = Parameter(gt=0, le=100, default=10),
        page: int = Parameter(ge=1, default=1),
        user_id: UUID = Parameter(default=None),
        status: str = Parameter(default=""),
    ) -> List[OrderResponse]:
        """Получить все заказы с пагинацией и фильтрацией"""
        filters = {}
        if user_id:
            filters["user_id"] = user_id
        if status:
            filters["status"] = status
            
        orders = await order_service.get_by_filter(db_session, count, page, **filters)
        return [OrderResponse.model_validate(order) for order in orders]

    @get("/{order_id:uuid}")
    async def get_order_by_id(
        self,
        order_service: OrderService,
        db_session: AsyncSession,
        order_id: UUID = Parameter(),
    ) -> OrderResponse:
        """Получить заказ по ID"""
        order = await order_service.get_by_id(db_session, order_id)
        if not order:
            from litestar.exceptions import NotFoundException
            raise NotFoundException(detail=f"Order with ID {order_id} not found")
        return OrderResponse.model_validate(order)

    @post("/")
    async def create_order(
        self,
        order_service: OrderService,
        db_session: AsyncSession,
        data: OrderCreate,
    ) -> OrderResponse:
        """Создать новый заказ"""        
        order = await order_service.create_order(db_session, data)
        await db_session.commit()
        return OrderResponse.model_validate(order)

    @put("/{order_id:uuid}")
    async def update_order(
        self,
        order_service: OrderService,
        db_session: AsyncSession,
        data: OrderUpdate,
        order_id: UUID = Parameter(),
    ) -> OrderResponse:
        """Обновить заказ"""       
        order = await order_service.update(db_session, order_id, data)
        await db_session.commit()
        return OrderResponse.model_validate(order)

    @delete("/{order_id:uuid}")
    async def delete_order(
        self,
        order_service: OrderService,
        db_session: AsyncSession,
        order_id: UUID = Parameter(),
    ) -> dict:
        """Удалить заказ"""
        result = await order_service.delete(db_session, order_id)
        await db_session.commit()
        if not result:
            from litestar.exceptions import NotFoundException
            raise NotFoundException(detail=f"Order with ID {order_id} not found")
        return {"message": "Order deleted successfully"}