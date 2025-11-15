from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: uuid.UUID
    quantity: int


class OrderItemResponse(OrderItemBase):
    price_at_order: float


class OrderBase(BaseModel):
    user_id: uuid.UUID
    address_id: Optional[uuid.UUID] = None
    items: List[OrderItemBase] = []
    total_price: float = 0.0
    status: str = 'pending'


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    user_id: Optional[uuid.UUID] = None
    address_id: Optional[uuid.UUID] = None
    total_price: Optional[float] = None
    status: Optional[str] = None


class OrderResponse(OrderBase):
    id: uuid.UUID
    order_date: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True