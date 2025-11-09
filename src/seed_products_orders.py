"""
Добавляет только товары и заказы.
Не трогает таблицы users / addresses.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --------------------------------------------------------------------
# 1. Строка подключения (точно такая же, как в seed.py)
# --------------------------------------------------------------------

DATABASE_URL = "sqlite:///./data.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# --------------------------------------------------------------------
# 2. Импорт моделей
# --------------------------------------------------------------------

from src.models import User, Address, Product, Order

def seed_products_and_orders():
    with SessionLocal() as session:
        # ------------------------------------------------------------
        # 3. Добавляем товары (если они ещё не созданы)
        # ------------------------------------------------------------
        products = []
        for i in range(1, 6):
            prod = session.query(Product).filter_by(name=f"Product {i}").first()
            if not prod:
                prod = Product(
                    name=f"Product {i}",
                    description=f"Описание продукта №{i}.",
                    price=10 * i
                )
                session.add(prod)
            products.append(prod)

        # ------------------------------------------------------------
        # 4. Добавляем заказы (один на каждого пользователя)
        # ------------------------------------------------------------
        users = session.query(User).all()
        for user in users:
            # Берём первый primary‑адрес у пользователя
            address = (
                session.query(Address)
                .filter_by(user_id=user.id, is_primary=True)
                .first()
            )
            if not address:
                continue  # если у пользователя нет primary адреса

            # Проверяем, не существует ли уже такой заказ (по user+address+product)
            existing_order = (
                session.query(Order)
                .filter_by(user_id=user.id,
                           address_id=address.id,
                           product_id=products[0].id)
                .first()
            )
            if existing_order:
                continue  # заказ уже есть

            order = Order(
                user_id=user.id,
                address_id=address.id,
                product_id=products[0].id,
                quantity=1,
                total_price=products[0].price,
                status="pending",
                order_date=datetime.now(timezone.utc)
            )
            session.add(order)

        session.commit()
        print(f"✅ Добавлено {len(products)} товаров и "
              f"{len(users)} заказов (если их ещё не было).")

# --------------------------------------------------------------------
# 5. Точка входа
# --------------------------------------------------------------------

if __name__ == "__main__":
    seed_products_and_orders()
