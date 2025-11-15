import pytest
from app.repositories.order_repository import OrderRepository
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository


class TestOrderRepository:
    @pytest.mark.asyncio
    async def test_create_order(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository):
        """Тест создания заказа в репозитории"""
        # Создаем пользователя и продукт для теста
        user = await user_repository.create({
            "username": "order_test_user",
            "email": "order_test@example.com"
        })
        
        product = await product_repository.create(
            name="Order Test Product",
            price=59.99,
            description="Order test description",
            stock_quantity=15
        )
        
        # Создаем заказ с элементами
        order = await order_repository.create(
            user_id=user.id,
            items=[{"product_id": product.id, "quantity": 2}],
            total_price=19.98,
            status="pending"
        )
        
        assert order.id is not None
        assert order.user_id == user.id
        assert order.total_price == 19.98
        assert order.status == "pending"

    @pytest.mark.asyncio
    async def test_get_order_by_id(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository):
        """Тест получения заказа по ID"""
        # Создаем пользователя и продукт для теста
        user = await user_repository.create({
            "username": "get_order_test_user",
            "email": "get_order_test@example.com"
        })
        
        product = await product_repository.create(
            name="Get Order Test Product",
            price=49.99,
            description="Get order test description",
            stock_quantity=10
        )
        
        created_order = await order_repository.create(
            user_id=user.id,
            items=[{"product_id": product.id, "quantity": 1}],
            total_price=49.99,
            status="pending"
        )

        found_order = await order_repository.get_by_id(created_order.id)
        assert found_order is not None
        assert found_order.id == created_order.id
        assert found_order.user_id == user.id

    @pytest.mark.asyncio
    async def test_get_order_by_filter(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository):
        """Тест получения заказов по фильтру"""
        # Создаем пользователя и продукт для теста
        user = await user_repository.create({
            "username": "filter_order_test_user",
            "email": "filter_order_test@example.com"
        })
        
        product = await product_repository.create(
            name="Filter Order Test Product",
            price=39.99,
            description="Filter order test description",
            stock_quantity=8
        )
        
        # Создаем несколько заказов
        await order_repository.create(
            user_id=user.id,
            items=[{"product_id": product.id, "quantity": 1}],
            total_price=39.99,
            status="pending"
        )
        
        await order_repository.create(
            user_id=user.id,
            items=[{"product_id": product.id, "quantity": 2}],
            total_price=79.98,
            status="completed"
        )

        # Получаем заказы с фильтрацией по пользователю
        orders = await order_repository.get_by_filter(count=10, page=1, user_id=user.id)
        assert len(orders) >= 2

        # Получаем заказы с фильтрацией по статусу
        orders = await order_repository.get_by_filter(count=10, page=1, status="completed")
        assert len(orders) >= 1
        for order in orders:
            assert order.status == "completed"

    @pytest.mark.asyncio
    async def test_update_order(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository):
        """Тест обновления заказа"""
        # Создаем пользователя и продукт для теста
        user = await user_repository.create({
            "username": "update_order_test_user",
            "email": "update_order_test@example.com"
        })
        
        product = await product_repository.create(
            name="Update Order Test Product",
            price=29.99,
            description="Update order test description",
            stock_quantity=5
        )
        
        order = await order_repository.create(
            user_id=user.id,
            items=[{"product_id": product.id, "quantity": 1}],
            total_price=29.99,
            status="pending"
        )

        updated_order = await order_repository.update(
            order.id,
            status="shipped"
        )

        assert updated_order.status == "shipped"  # Изменилось
        assert updated_order.user_id == user.id  # Осталось без изменений
        assert updated_order.total_price == 29.99 # Осталось без изменений

    @pytest.mark.asyncio
    async def test_delete_order(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository):
        """Тест удаления заказа"""
        # Создаем пользователя и продукт для теста
        user = await user_repository.create({
            "username": "delete_order_test_user",
            "email": "delete_order_test@example.com"
        })
        
        product = await product_repository.create(
            name="Delete Order Test Product",
            price=19.99,
            description="Delete order test description",
            stock_quantity=3
        )
        
        order = await order_repository.create(
            user_id=user.id,
            items=[{"product_id": product.id, "quantity": 1}],
            total_price=19.99,
            status="pending"
        )
        assert order is not None

        # Удаляем заказ
        result = await order_repository.delete(order.id)
        assert result is True

        # Проверяем, что заказ удален
        deleted_order = await order_repository.get_by_id(order.id)
        assert deleted_order is None