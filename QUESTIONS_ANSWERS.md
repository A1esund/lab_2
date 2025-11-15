# Ответы на вопросы из лабораторной работы №4

## 1. Почему в тестах мы используем отдельную тестовую базу данных (SQLite in-memory)? Какие проблемы могут возникнуть при использовании production базы данных для тестирования?

Использование отдельной тестовой базы данных необходимо по нескольким причинам:

- **Изоляция тестов**: каждый тест может начинать с чистого состояния базы данных, что позволяет избежать влияния одного теста на другой
- **Безопасность**: тесты не могут случайно повредить или изменить реальные данные в production базе
- **Предсказуемость**: тесты будут давать одинаковые результаты при каждом запуске, так как стартуют с одинакового начального состояния
- **Скорость**: тестовая база данных может быть оптимизирована для быстрого выполнения тестов (например, SQLite in-memory работает быстрее, чем полноценная БД)
- **Воспроизводимость**: ошибки, найденные в тестах, можно будет воспроизвести в любом окружении

При использовании production базы данных могут возникнуть следующие проблемы:
- Повреждение реальных данных
- Нарушение целостности данных
- Непредсказуемые результаты тестов из-за изменений в production
- Невозможность тестирования сценариев удаления данных
- Проблемы с безопасностью и доступом

## 2. Как работает `TestClient` в Litestar? Какие преимущества он дает по сравнению с обычными HTTP-запросами?

`TestClient` в Litestar - это инструмент для тестирования веб-приложений, который работает следующим образом:

- Он создает тестовую среду, которая имитирует реальный сервер
- Позволяет выполнять HTTP-запросы к приложению без запуска реального сервера
- Обрабатывает запросы напрямую в памяти, что делает тесты быстрее
- Предоставляет удобный интерфейс для проверки ответов, статус-кодов, заголовков и тела ответа

Преимущества по сравнению с обычными HTTP-запросами:
- **Скорость**: не требуется запускать реальный сервер, тесты выполняются быстрее
- **Изоляция**: тесты не зависят от внешних факторов, таких как сеть или состояние сервера
- **Контроль**: можно легко настраивать окружение и зависимости для каждого теста
- **Безопасность**: не требуется открывать порты или настраивать доступ
- **Отладка**: легче отлаживать проблемы, так как все происходит в памяти

## 3. При тестировании сервиса заказов, какие edge cases (граничные случаи) нужно учитывать? Напишите к ним тесты.

При тестировании сервиса заказов нужно учитывать следующие граничные случаи:

- **Недостаточное количество товара на складе**: тест уже реализован в `tests/test_order_service.py`
- **Попытка создать заказ с несуществующим пользователем**
- **Попытка создать заказ с несуществующим продуктом**
- **Попытка создать заказ с отрицательным количеством товара**
- **Попытка создать заказ с нулевым количеством товара**
- **Попытка обновить заказ в несуществующий статус**
- **Создание заказа с пустым списком товаров**
- **Обновление заказа после его завершения/отмены**

Тесты для некоторых из этих случаев:

```python
@pytest.mark.asyncio
async def test_create_order_with_nonexistent_user(self):
    """Тест создания заказа с несуществующим пользователем"""
    mock_user_repo = AsyncMock(spec=OrderService)
    mock_product_repo = AsyncMock(spec=OrderService)
    mock_order_repo = AsyncMock(spec=OrderService)

    mock_user_repo.get_by_id.return_value = None  # Пользователь не найден

    order_service = OrderService(
        order_repository=mock_order_repo,
        user_repository=mock_user_repo,
        product_repository=mock_product_repo
    )

    order_data = Mock()
    order_data.user_id = 999  # Не существующий ID
    order_data.items = [Mock(product_id=1, quantity=2)]
    order_data.total_price = 200.0
    order_data.status = "pending"

    with pytest.raises(ValueError, match="User with id 999 not found"):
        await order_service.create_order(None, order_data)

@pytest.mark.asyncio
async def test_create_order_with_nonexistent_product(self):
    """Тест создания заказа с несуществующим продуктом"""
    mock_user_repo = AsyncMock(spec=OrderService)
    mock_product_repo = AsyncMock(spec=OrderService)
    mock_order_repo = AsyncMock(spec=OrderService)

    mock_user_repo.get_by_id.return_value = Mock(id=1)
    mock_product_repo.get_by_id.return_value = None  # Продукт не найден

    order_service = OrderService(
        order_repository=mock_order_repo,
        user_repository=mock_user_repo,
        product_repository=mock_product_repo
    )

    order_data = Mock()
    order_data.user_id = 1
    order_data.items = [Mock(product_id=999, quantity=2)]  # Не существующий продукт
    order_data.total_price = 200.0
    order_data.status = "pending"

    with pytest.raises(ValueError, match="Product with id 99 not found"):
        await order_service.create_order(None, order_data)
```

## 4. Как бы вы протестировали метод, который должен отправлять email при смене статуса заказа на "shipped"?

Для тестирования метода, который отправляет email при смене статуса заказа на "shipped", я бы использовал следующий подход:

- **Мокирование сервиса отправки email**: чтобы не отправлять реальные письма во время тестов
- **Тестирование смены статуса заказа**: проверить, что статус действительно изменяется
- **Проверка вызова метода отправки email**: убедиться, что email отправляется только при смене статуса на "shipped"
- **Проверка содержания письма**: убедиться, что письмо содержит корректную информацию

Пример теста:

```python
@pytest.mark.asyncio
async def test_update_order_status_to_shipped_sends_email(self):
    """Тест обновления статуса заказа до shipped с отправкой email"""
    # Мокаем репозитории и сервис email
    mock_order_repo = AsyncMock()
    mock_user_repo = AsyncMock()
    mock_product_repo = AsyncMock()
    mock_email_service = AsyncMock()

    # Подготовим тестовые данные
    existing_order = Mock(id=1, user_id=1, status="processing")
    updated_order = Mock(id=1, user_id=1, status="shipped")
    
    mock_order_repo.get_by_id.return_value = existing_order
    mock_order_repo.update.return_value = updated_order
    mock_user_repo.get_by_id.return_value = Mock(email="customer@example.com")

    # Создаем сервис заказов с моками
    order_service = OrderService(
        order_repository=mock_order_repo,
        user_repository=mock_user_repo,
        product_repository=mock_product_repo
    )
    # Добавляем мок для email сервиса как атрибут
    order_service.email_service = mock_email_service

    # Обновляем статус до shipped
    result = await order_service.update(None, 1, Mock(status="shipped"))

    # Проверяем, что статус обновился
    assert result.status == "shipped"
    
    # Проверяем, что email был отправлен
    mock_email_service.send_order_shipped_email.assert_called_once_with(
        "customer@example.com", 
        existing_order
    )
```

## 5. Напишите тест для проверки пагинации товаров. Какие параметры должны проверяться?

При тестировании пагинации товаров нужно проверять следующие параметры:

- **Количество элементов на странице**: соответствует параметру `count`
- **Номер страницы**: корректное смещение элементов
- **Общее количество элементов**: правильное количество возвращаемых результатов
- **Пустые страницы**: корректное поведение при запросе несуществующей страницы
- **Фильтрация с пагинацией**: корректная работа фильтров при пагинации

Пример теста:

```python
@pytest.mark.asyncio
async def test_product_pagination(self, product_repository: ProductRepository):
    """Тест пагинации товаров"""
    # Создаем 25 тестовых продуктов
    for i in range(25):
        await product_repository.create(
            name=f"Test Product {i}",
            price=10.0 + i,
            description=f"Test description {i}",
            stock_quantity=10
        )

    # Тестируем первую страницу (10 элементов)
    first_page = await product_repository.get_by_filter(count=10, page=1)
    assert len(first_page) == 10
    assert first_page[0].name == "Test Product 0"
    assert first_page[9].name == "Test Product 9"

    # Тестируем вторую страницу (следующие 10 элементов)
    second_page = await product_repository.get_by_filter(count=10, page=2)
    assert len(second_page) == 10
    assert second_page[0].name == "Test Product 10"
    assert second_page[9].name == "Test Product 19"

    # Тестируем третью страницу (оставшиеся 5 элементов)
    third_page = await product_repository.get_by_filter(count=10, page=3)
    assert len(third_page) == 5
    assert third_page[0].name == "Test Product 20"

    # Тестируем несуществующую страницу (должна вернуть пустой список)
    empty_page = await product_repository.get_by_filter(count=10, page=10)
    assert len(empty_page) == 0
```

## 6. Как обеспечить изоляцию тестов друг от друга? Почему это важно?

Изоляция тестов важна по следующим причинам:

- **Предсказуемость**: каждый тест должен давать одинаковый результат независимо от порядка выполнения
- **Надежность**: ошибки в одном тесте не должны влиять на другие тесты
- **Повторяемость**: тесты должны быть воспроизводимы в любом окружении
- **Легкость отладки**: ошибки легче локализовать, когда тесты независимы

Способы обеспечения изоляции тестов:

- **Использование фикстур с правильным скоупом**: например, фикстура уровня функции для каждого теста
- **Очистка состояния после каждого теста**: удаление созданных данных
- **Использование отдельной тестовой базы данных**: каждый тест может начинать с чистого состояния
- **Создание независимых экземпляров сервисов**: чтобы избежать состояния между тестами
- **Использование моков**: чтобы избежать зависимости от внешних систем

Пример изоляции с использованием фикстур:

```python
@pytest.fixture
async def clean_database(engine):
    """Фикстура для очистки базы данных перед каждым тестом"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Очистка после теста
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)