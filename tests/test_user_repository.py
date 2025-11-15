import pytest
from app.models.user import User
from app.repositories.user_repository import UserRepository


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, user_repository: UserRepository):
        """Тест создания пользователя в репозитории"""
        user_data = {
            "username": "john_doe",
            "email": "test@example.com"
        }

        user = await user_repository.create(user_data)
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.username == "john_doe"

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, user_repository: UserRepository):
        """Тест получения пользователя по ID"""
        user_data = {
            "username": "jane_doe",
            "email": "jane@example.com"
        }

        created_user = await user_repository.create(user_data)

        found_user = await user_repository.get_by_id(created_user.id)
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == "jane@example.com"

    @pytest.mark.asyncio
    async def test_get_user_by_filter(self, user_repository: UserRepository):
        """Тест получения пользователей по фильтру"""
        # Создаем несколько пользователей
        user_data1 = {
            "username": "test_user_1",
            "email": "test1@example.com"
        }
        user_data2 = {
            "username": "test_user_2",
            "email": "test2@example.com"
        }

        await user_repository.create(user_data1)
        await user_repository.create(user_data2)

        # Получаем пользователей с фильтрацией
        users = await user_repository.get_by_filter(count=10, page=1, username="test_user_1")
        assert len(users) == 1
        assert users[0].username == "test_user_1"

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository: UserRepository):
        """Тест обновления пользователя"""
        user_data = {
            "username": "original_name",
            "email": "original@example.com"
        }

        user = await user_repository.create(user_data)

        updated_user = await user_repository.update(
            user.id,
            {"username": "updated_name"}
        )

        assert updated_user.username == "updated_name"  # Изменилось
        assert updated_user.email == "original@example.com"  # Осталось без изменений

    @pytest.mark.asyncio
    async def test_delete_user(self, user_repository: UserRepository):
        """Тест удаления пользователя"""
        user_data = {
            "username": "delete_test",
            "email": "delete@example.com"
        }

        user = await user_repository.create(user_data)
        assert user is not None

        # Удаляем пользователя
        result = await user_repository.delete(user.id)
        assert result is True

        # Проверяем, что пользователь удален
        deleted_user = await user_repository.get_by_id(user.id)
        assert deleted_user is None

    @pytest.mark.asyncio
    async def test_get_all_users(self, user_repository: UserRepository):
        """Тест получения всех пользователей"""
        # Создаем несколько пользователей
        for i in range(5):
            user_data = {
                "username": f"all_test_user_{i}",
                "email": f"all_test{i}@example.com"
            }
            await user_repository.create(user_data)

        # Получаем всех пользователей
        users = await user_repository.get_by_filter(count=10, page=1)
        assert len(users) >= 5