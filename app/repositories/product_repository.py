import uuid
from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Product


class ProductRepository:
    """Репозиторий для работы с продуктами"""
    
    async def get_by_id(self, session: AsyncSession, product_id: uuid.UUID) -> Optional[Product]:
        """Получить продукт по ID"""
        stmt = select(Product).where(Product.id == product_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_filter(self, session: AsyncSession, count: int, page: int, **kwargs) -> List[Product]:
        """Получить продукты по фильтрам с пагинацией"""
        stmt = select(Product)
        
        # Применяем фильтры
        if 'name' in kwargs and kwargs['name']:
            stmt = stmt.where(Product.name.ilike(f"%{kwargs['name']}%"))
        if 'min_price' in kwargs:
            stmt = stmt.where(Product.price >= kwargs['min_price'])
        if 'max_price' in kwargs:
            stmt = stmt.where(Product.price <= kwargs['max_price'])
        
        # Применяем пагинацию
        offset = (page - 1) * count
        stmt = stmt.offset(offset).limit(count)
        
        result = await session.execute(stmt)
        return result.scalars().all()
    
    async def create(self, session: AsyncSession, name: str, price: float, description: Optional[str] = None, stock_quantity: int = 0) -> Product:
        """Создать новый продукт"""
        product = Product(
            name=name,
            price=price,
            description=description,
            stock_quantity=stock_quantity
        )
        session.add(product)
        await session.flush()
        await session.refresh(product)
        return product
    
    async def update(self, session: AsyncSession, product_id: uuid.UUID, **kwargs) -> Product:
        """Обновить продукт"""
        # Собираем только те поля, которые были переданы
        update_data = {}
        if 'name' in kwargs and kwargs['name'] is not None:
            update_data['name'] = kwargs['name']
        if 'price' in kwargs and kwargs['price'] is not None:
            update_data['price'] = kwargs['price']
        if 'description' in kwargs and kwargs['description'] is not None:
            update_data['description'] = kwargs['description']
        if 'stock_quantity' in kwargs and kwargs['stock_quantity'] is not None:
            update_data['stock_quantity'] = kwargs['stock_quantity']
        
        if not update_data:
            # Если нет данных для обновления, возвращаем продукт без изменений
            product = await self.get_by_id(session, product_id)
            if not product:
                raise ValueError(f"Product with id {product_id} not found")
            return product
        
        stmt = update(Product).where(Product.id == product_id).values(**update_data)
        await session.execute(stmt)
        
        # Получаем обновленный продукт
        product = await self.get_by_id(session, product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")
        return product
    
    async def delete(self, session: AsyncSession, product_id: uuid.UUID) -> bool:
        """Удалить продукт"""
        product = await self.get_by_id(session, product_id)
        if not product:
            return False
            
        stmt = delete(Product).where(Product.id == product_id)
        await session.execute(stmt)
        return True