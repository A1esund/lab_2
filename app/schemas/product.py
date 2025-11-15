from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    stock_quantity: int = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock_quantity: Optional[int] = None


class ProductResponse(ProductBase):
    id: uuid.UUID

    class Config:
        from_attributes = True