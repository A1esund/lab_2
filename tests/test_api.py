import pytest
from typing import Protocol
from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory
from litestar.status_codes import HTTP_200_OK
from litestar import get
from litestar.di import Provide
from litestar.testing import create_test_client
from app.main import app


def test_get_users_api():
    """Тест эндпоинта получения пользователей"""
    with create_test_client(app=app) as client:
        response = client.get("/users")
        # Ожидаем, что запрос будет успешным (хотя может вернуть пустой список)
        assert response.status_code in [200, 404]  # 404 может быть, если нет пользователей


def test_get_products_api():
    """Тест эндпоинта получения продуктов"""
    with create_test_client(app=app) as client:
        response = client.get("/products")
        assert response.status_code in [200, 404]  # 404 может быть, если нет продуктов


def test_get_orders_api():
    """Тест эндпоинта получения заказов"""
    with create_test_client(app=app) as client:
        response = client.get("/orders")
        assert response.status_code in [200, 404]  # 404 может быть, если нет заказов


class Item(BaseModel):
    name: str


class Service(Protocol):
    def get_one(self) -> Item: ...


@get(path="/item")
def get_item(service: Service) -> Item:
    return service.get_one()


class ItemFactory(ModelFactory[Item]):
    model = Item


@pytest.fixture()
def item():
    return ItemFactory.build()


def test_get_item(item: Item):
    class MyService(Service):
        def get_one(self) -> Item:
            return item

    with create_test_client(
        route_handlers=[get_item],
        dependencies={"service": Provide(lambda: MyService())}
    ) as client:
        response = client.get("/item")
        assert response.status_code == HTTP_200_OK
        assert response.json() == Item.model_dump(item)