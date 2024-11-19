import unittest
from unittest.mock import patch, MagicMock
from app.services.user_service import UserService
from app.models.user import User
from app.extensions import db, cache
from app import create_app


class TestUserService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем приложение и устанавливаем контекст."""
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/flask_db'
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        """Удаляем контекст приложения после завершения тестов."""
        cls.app_context.pop()

    def setUp(self):
        self.service = UserService()

    @patch('app.models.user.User.query')
    def test_get_all_users(self, mock_query):
        # Настраиваем mock для возврата списка пользователей
        mock_query.all.return_value = [User(id=1, username="test", email="L5eG8@example.com")]

        # Чистить кэш перед вызовом метода
        cache.clear()

        # Вызываем метод
        users = self.service.get_all_users()

        # Проверяем результаты
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, "test")
        self.assertEqual(users[0].email, "L5eG8@example.com")
        mock_query.all.assert_called_once()

    @patch('app.models.user.User.query')
    def test_get_user_by_id(self, mock_query):
        # Настраиваем mock для возврата конкретного пользователя
        mock_query.get_or_404.return_value = User(id=1, username="test", email="L5eG8@example.com")

        # Вызываем метод
        user = self.service.get_user_by_id(1)

        # Проверяем результаты
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "test")
        mock_query.get_or_404.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
