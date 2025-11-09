"""
Минимальный скрипт заполнения БД тестовыми данными.
"""

import uuid
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --------------------------------------------------------------------
# 1. Строка подключения
# --------------------------------------------------------------------

DATABASE_URL = "sqlite:///./data.db"

# --------------------------------------------------------------------
# 2. Создаём engine и фабрику сессий
# --------------------------------------------------------------------

engine = create_engine(DATABASE_URL, echo=True)   # echo=True – выводит SQL‑запросы
SessionLocal = sessionmaker(bind=engine)

# --------------------------------------------------------------------
# 3. Импортируем модели (они уже объявлены в src/models.py)
# --------------------------------------------------------------------

from src.models import User, Address

# --------------------------------------------------------------------
# 4. Функция заполнения
# --------------------------------------------------------------------

def seed():
    with SessionLocal() as session:
        # Создаём пользователей
        users = []
        for i in range(1, 6):          # 5 пользователей
            user = User(
                username=f"user{i}",
                email=f"user{i}@example.com",
            )
            session.add(user)
            users.append(user)

        # Получаем id после flush (или commit), чтобы можно было использовать их в адресах
        session.flush()

        # Добавляем два адреса для каждого пользователя
        for idx, user in enumerate(users, start=1):
            addr1 = Address(
                user_id=user.id,
                street=f"{idx} Main St",
                city="Moscow",
                state="",
                zip_code="101000",
                country="Russia",
                is_primary=True,
                updated_at=datetime.now()
            )
            session.add(addr1)

            addr2 = Address(
                user_id=user.id,
                street=f"{idx} Second St",
                city="Saint Petersburg",
                state="",
                zip_code="190000",
                country="Russia",
                is_primary=False,
                updated_at=datetime.now()
            )
            session.add(addr2)
        session.commit()

        # Автоматически коммитится при выходе из блока
        print(f"✅ Добавлено {len(users)} пользователей и {len(users)*2} адресов.")

# --------------------------------------------------------------------
# 5. Точка входа
# --------------------------------------------------------------------

if __name__ == "__main__":
    seed()
