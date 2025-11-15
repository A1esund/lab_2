from typing import List
from uuid import UUID
from litestar import Controller, get, post, put, delete, patch
from litestar.di import Provide
from litestar.params import Parameter
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService


class ProductController(Controller):
    path = "/products"
    
    def __init__(self):
        self.dependencies = {
            "product_service": Provide(lambda: ProductService()),
        }

    @get("/")
    async def get_all_products(
        self,
        product_service: ProductService,
        db_session: AsyncSession,
        count: int = Parameter(gt=0, le=100, default=10),
        page: int = Parameter(ge=1, default=1),
        name: str = Parameter(default=""),
        min_price: float = Parameter(default=None),
        max_price: float = Parameter(default=None),
    ) -> List[ProductResponse]:
        """Получить все продукты с пагинацией и фильтрацией"""
        filters = {}
        if name:
            filters["name"] = name
        if min_price is not None:
            filters["min_price"] = min_price
        if max_price is not None:
            filters["max_price"] = max_price
            
        products = await product_service.get_by_filter(db_session, count, page, **filters)
        return [ProductResponse.model_validate(product) for product in products]

    @get("/{product_id:uuid}")
    async def get_product_by_id(
        self,
        product_service: ProductService,
        db_session: AsyncSession,
        product_id: UUID = Parameter(),
    ) -> ProductResponse:
        """Получить продукт по ID"""
        product = await product_service.get_by_id(db_session, product_id)
        if not product:
            from litestar.exceptions import NotFoundException
            raise NotFoundException(detail=f"Product with ID {product_id} not found")
        return ProductResponse.model_validate(product)

    @post("/")
    async def create_product(
        self,
        product_service: ProductService,
        db_session: AsyncSession,
        data: ProductCreate,
    ) -> ProductResponse:
        """Создать новый продукт"""        
        product = await product_service.create(db_session, data)
        await db_session.commit()
        return ProductResponse.model_validate(product)

    @put("/{product_id:uuid}")
    async def update_product(
        self,
        product_service: ProductService,
        db_session: AsyncSession,
        data: ProductUpdate,
        product_id: UUID = Parameter(),
    ) -> ProductResponse:
        """Обновить продукт"""       
        product = await product_service.update(db_session, product_id, data)
        await db_session.commit()
        return ProductResponse.model_validate(product)

    @delete("/{product_id:uuid}")
    async def delete_product(
        self,
        product_service: ProductService,
        db_session: AsyncSession,
        product_id: UUID = Parameter(),
    ) -> dict:
        """Удалить продукт"""
        result = await product_service.delete(db_session, product_id)
        await db_session.commit()
        if not result:
            from litestar.exceptions import NotFoundException
            raise NotFoundException(detail=f"Product with ID {product_id} not found")
        return {"message": "Product deleted successfully"}