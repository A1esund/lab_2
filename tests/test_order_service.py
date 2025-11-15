import pytest
from unittest.mock import Mock, AsyncMock
from app.services.order_service import OrderService


class TestOrderService:
    @pytest.mark.asyncio
    async def test_create_order_success(self):
        """Тест успешного создания заказа"""
        # Мокаем репозитории
        mock_order_repo = AsyncMock(spec=OrderService)
        mock_product_repo = AsyncMock(spec=OrderService)
        mock_user_repo = AsyncMock(spec=OrderService)

        # Настраиваем поведение моков
        mock_user_repo.get_by_id.return_value = Mock(id=1, email="test@example.com")
        mock_product_repo.get_by_id.return_value = Mock(id=1, name="Test Product", price=100.0, stock_quantity=5)
        mock_order_repo.create.return_value = Mock(id=1, user_id=1, total_amount=200.0, status="pending")

        # Создаем сервис с моками
        order_service = OrderService(
            order_repository=mock_order_repo,
            user_repository=mock_user_repo,
            product_repository=mock_product_repo
        )

        # Данные для заказа
        order_data = Mock()
        order_data.user_id = 1
        order_data.items = [Mock(product_id=1, quantity=2)]
        order_data.total_price = 200.0
        order_data.status = "pending"

        result = await order_service.create_order(None, order_data)

        assert result is not None
        # assert result.total_amount == 200.0
        mock_order_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_order_insufficient_stock(self):
        """Тест создания заказа с недостаточным количеством товара"""
        mock_user_repo = AsyncMock(spec=OrderService)
        mock_product_repo = AsyncMock(spec=OrderService)
        mock_order_repo = AsyncMock(spec=OrderService)

        mock_user_repo.get_by_id.return_value = Mock(id=1)
        mock_product_repo.get_by_id.return_value = Mock(id=1, name="Test Product", price=100.0, stock_quantity=1)

        order_service = OrderService(
            order_repository=mock_order_repo,
            user_repository=mock_user_repo,
            product_repository=mock_product_repo
        )

        order_data = Mock()
        order_data.user_id = 1
        order_data.items = [Mock(product_id=1, quantity=5)]  # Запрашиваем больше, чем есть на складе
        order_data.total_price = 500.0
        order_data.status = "pending"

        with pytest.raises(ValueError, match="Insufficient stock"):
            await order_service.create_order(None, order_data)