import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from src.models import Product


class ProductService:
    """Бизнес-логика управления продуктами."""

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_by_id(
        self,
        session: AsyncSession,
        product_id: uuid.UUID,
    ) -> Optional[Product]:
        """Получить продукт по его UUID."""
        return await self.product_repository.get_by_id(session, product_id)

    async def get_by_filter(
        self,
        session: AsyncSession,
        count: int,
        page: int,
        **kwargs,
    ) -> List[Product]:
        """Получить продукты по фильтрам с пагинацией."""
        return await self.product_repository.get_by_filter(session, count, page, **kwargs)

    async def create(
        self,
        session: AsyncSession,
        product_data: ProductCreate,
    ) -> Product:
        """Создать новый продукт."""
        return await self.product_repository.create(
            session,
            name=product_data.name,
            price=product_data.price,
            description=product_data.description,
            stock_quantity=product_data.stock_quantity
        )

    async def update(
        self,
        session: AsyncSession,
        product_id: uuid.UUID,
        product_data: ProductUpdate,
    ) -> Product:
        """Обновить существующий продукт."""
        # Собираем только те поля, которые были переданы
        update_data = {}
        if product_data.name is not None:
            update_data['name'] = product_data.name
        if product_data.price is not None:
            update_data['price'] = product_data.price
        if product_data.description is not None:
            update_data['description'] = product_data.description
        if product_data.stock_quantity is not None:
            update_data['stock_quantity'] = product_data.stock_quantity
        
        product = await self.product_repository.update(session, product_id, **update_data)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")
        return product

    async def delete(
        self,
        session: AsyncSession,
        product_id: uuid.UUID,
    ) -> bool:
        """Удалить продукт по его UUID."""
        return await self.product_repository.delete(session, product_id)