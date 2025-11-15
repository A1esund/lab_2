import pytest
from app.repositories.product_repository import ProductRepository


class TestProductRepository:
    @pytest.mark.asyncio
    async def test_create_product(self, product_repository: ProductRepository):
        """Тест создания продукта в репозитории"""
        product = await product_repository.create(
            name="Test Product",
            price=99.99,
            description="Test description",
            stock_quantity=10
        )
        
        assert product.id is not None
        assert product.name == "Test Product"
        assert product.price == 9.99
        assert product.description == "Test description"
        assert product.stock_quantity == 10

    @pytest.mark.asyncio
    async def test_get_product_by_id(self, product_repository: ProductRepository):
        """Тест получения продукта по ID"""
        created_product = await product_repository.create(
            name="Get Test Product",
            price=49.99,
            description="Get test description",
            stock_quantity=5
        )

        found_product = await product_repository.get_by_id(created_product.id)
        assert found_product is not None
        assert found_product.id == created_product.id
        assert found_product.name == "Get Test Product"

    @pytest.mark.asyncio
    async def test_get_product_by_filter(self, product_repository: ProductRepository):
        """Тест получения продуктов по фильтру"""
        # Создаем несколько продуктов
        await product_repository.create(
            name="Filter Test Product 1",
            price=29.99,
            description="Filter test 1",
            stock_quantity=3
        )
        await product_repository.create(
            name="Filter Test Product 2", 
            price=39.99,
            description="Filter test 2",
            stock_quantity=7
        )

        # Получаем продукты с фильтрацией по названию
        products = await product_repository.get_by_filter(count=10, page=1, name="Filter Test Product 1")
        assert len(products) == 1
        assert products[0].name == "Filter Test Product 1"

        # Получаем продукты с фильтрацией по диапазону цен
        products = await product_repository.get_by_filter(count=10, page=1, min_price=30, max_price=40)
        assert len(products) >= 1
        for product in products:
            assert 30 <= product.price <= 40

    @pytest.mark.asyncio
    async def test_update_product(self, product_repository: ProductRepository):
        """Тест обновления продукта"""
        product = await product_repository.create(
            name="Original Product",
            price=19.99,
            description="Original description",
            stock_quantity=8
        )

        updated_product = await product_repository.update(
            product.id,
            name="Updated Product",
            price=29.99
        )

        assert updated_product.name == "Updated Product"  # Изменилось
        assert updated_product.price == 29.99  # Изменилось
        assert updated_product.description == "Original description"  # Осталось без изменений
        assert updated_product.stock_quantity == 8  # Осталось без изменений

    @pytest.mark.asyncio
    async def test_delete_product(self, product_repository: ProductRepository):
        """Тест удаления продукта"""
        product = await product_repository.create(
            name="Delete Test Product",
            price=15.99,
            description="Delete test description",
            stock_quantity=4
        )
        assert product is not None

        # Удаляем продукт
        result = await product_repository.delete(product.id)
        assert result is True

        # Проверяем, что продукт удален
        deleted_product = await product_repository.get_by_id(product.id)
        assert deleted_product is None