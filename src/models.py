import uuid
from datetime import datetime
from typing import Optional, List

import sqlalchemy as sa

from sqlalchemy import ForeignKey, DateTime, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now) 		
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    description: Mapped[str | None] = mapped_column(
    nullable=True,          # можно хранить NULL, если описание не задано
    default=None            # при создании записи будет set на None
    )

    # -----------------------------------------------------------------
    # Связи (1 → N): пользователь имеет несколько заказов и адресов
    # -----------------------------------------------------------------
    orders: Mapped[List["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column(nullable=False)
    is_primary: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now) 
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now)

    # -----------------------------------------------------------------
    # Связи
    # -----------------------------------------------------------------
    user: Mapped["User"] = relationship(back_populates="addresses")
    orders: Mapped[List["Order"]] = relationship(
        back_populates="address",
        cascade="all, delete-orphan"
    )

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    price: Mapped[float] = mapped_column(nullable=False)          # в валюте вашего проекта
    description: Mapped[Optional[str]] = mapped_column(sa.Text, nullable=True)

    # -----------------------------------------------------------------
    # Связи
    # -----------------------------------------------------------------
    orders: Mapped[List["Order"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )


# -------------------------------------------------------------
# 4. Заказ (orders)
# -------------------------------------------------------------
class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('users.id', ondelete='CASCADE')
    )
    address_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('addresses.id', ondelete='SET NULL'),
        nullable=True   # адрес может быть удалён, но заказ останется
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('products.id', ondelete='CASCADE')
    )

    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    total_price: Mapped[float] = mapped_column(nullable=False)  # price * quantity

    status: Mapped[str] = mapped_column(
        sa.String(50),
        nullable=False,
        default='pending'
    )

    order_date: Mapped[datetime] = mapped_column(
    sa.DateTime(),
    server_default=sa.func.now(),   # автоматически ставит CURRENT_TIMESTAMP
    nullable=False
    )

    # -----------------------------------------------------------------
    # Связи
    # -----------------------------------------------------------------
    user: Mapped["User"] = relationship(back_populates="orders")
    address: Mapped[Optional["Address"]] = relationship(back_populates="orders")
    product: Mapped["Product"] = relationship(back_populates="orders")