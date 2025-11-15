import uuid
from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Order, User, Product, order_items


class OrderRepository:
    """Репозиторий для работы с заказами"""
    
    async def get_by_id(self, session: AsyncSession, order_id: uuid.UUID) -> Optional[Order]:
        """Получить заказ по ID"""
        stmt = select(Order).where(Order.id == order_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_filter(self, session: AsyncSession, count: int, page: int, **kwargs) -> List[Order]:
        """Получить заказы по фильтрам с пагинацией"""
        stmt = select(Order)
        
        # Применяем фильтры
        if 'user_id' in kwargs and kwargs['user_id']:
            stmt = stmt.where(Order.user_id == kwargs['user_id'])
        if 'status' in kwargs and kwargs['status']:
            stmt = stmt.where(Order.status == kwargs['status'])
        
        # Применяем пагинацию
        offset = (page - 1) * count
        stmt = stmt.offset(offset).limit(count)
        
        result = await session.execute(stmt)
        return result.scalars().all()
    
    async def create(self, session: AsyncSession, user_id: uuid.UUID, address_id: Optional[uuid.UUID] = None, 
                     items: Optional[List[dict]] = None, total_price: float = 0.0, status: str = 'pending') -> Order:
        """Создать новый заказ"""
        order = Order(
            user_id=user_id,
            address_id=address_id,
            total_price=total_price,
            status=status
        )
        
        session.add(order)
        await session.flush()
        await session.refresh(order)
        
        # Если переданы элементы заказа, добавляем их
        if items:
            for item in items:
                product_id = item['product_id']
                quantity = item['quantity']
                
                # Получаем продукт для получения цены на момент заказа
                product = await session.get(Product, product_id)
                if product:
                    # Проверяем, достаточно ли товара на складе
                    if product.stock_quantity >= quantity:
                        # Уменьшаем количество товара на складе
                        product.stock_quantity -= quantity
                        
                        # Добавляем запись в промежуточную таблицу
                        stmt = order_items.insert().values(
                            order_id=order.id,
                            product_id=product_id,
                            quantity=quantity,
                            price_at_order=product.price
                        )
                        await session.execute(stmt)
                        
                        # Обновляем общую стоимость заказа
                        order.total_price += product.price * quantity
                    else:
                        raise ValueError(f"Not enough stock for product {product_id}")
        
        await session.flush()
        await session.refresh(order)
        return order
    
    async def update(self, session: AsyncSession, order_id: uuid.UUID, **kwargs) -> Order:
        """Обновить заказ"""
        # Собираем только те поля, которые были переданы
        update_data = {}
        if 'user_id' in kwargs and kwargs['user_id'] is not None:
            update_data['user_id'] = kwargs['user_id']
        if 'address_id' in kwargs and kwargs['address_id'] is not None:
            update_data['address_id'] = kwargs['address_id']
        if 'total_price' in kwargs and kwargs['total_price'] is not None:
            update_data['total_price'] = kwargs['total_price']
        if 'status' in kwargs and kwargs['status'] is not None:
            update_data['status'] = kwargs['status']
        
        if not update_data:
            # Если нет данных для обновления, возвращаем заказ без изменений
            order = await self.get_by_id(session, order_id)
            if not order:
                raise ValueError(f"Order with id {order_id} not found")
            return order
        
        stmt = update(Order).where(Order.id == order_id).values(**update_data)
        await session.execute(stmt)
        
        # Получаем обновленный заказ
        order = await self.get_by_id(session, order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found")
        return order
    
    async def delete(self, session: AsyncSession, order_id: uuid.UUID) -> bool:
        """Удалить заказ"""
        order = await self.get_by_id(session, order_id)
        if not order:
            return False
            
        stmt = delete(Order).where(Order.id == order_id)
        await session.execute(stmt)
        return True