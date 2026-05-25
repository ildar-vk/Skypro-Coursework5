from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты модели Habit."""

    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com', password='Test12345')
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00',
            action='Чтение',
            is_pleasant=True,
            duration_seconds=60
        )
        self.useful_habit = Habit.objects.create(
            user=self.user,
            place='Улица',
            time='08:00',
            action='Зарядка',
            related_habit=self.pleasant_habit,
            duration_seconds=60
        )

    def test_habit_creation(self):
        self.assertEqual(self.useful_habit.action, 'Зарядка')
        self.assertEqual(self.useful_habit.place, 'Улица')

    def test_pleasant_habit_no_reward(self):
        self.assertFalse(self.pleasant_habit.reward)
        self.assertIsNone(self.pleasant_habit.related_habit)

    def test_str_method(self):
        self.assertIn('Зарядка', str(self.useful_habit))
        self.assertIn('Улица', str(self.useful_habit))


class HabitValidatorTest(TestCase):
    """Тесты валидации привычек."""

    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com', password='Test12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_reward_and_related_habit_conflict(self):
        """Нельзя одновременно reward и related_habit."""
        pleasant = Habit.objects.create(
            user=self.user, place='Дом', time='10:00',
            action='Сон', is_pleasant=True, duration_seconds=60
        )
        response = self.client.post('/api/habits/', {
            'place': 'Дом', 'time': '08:00', 'action': 'Тест',
            'reward': 'Конфета', 'related_habit': pleasant.id, 'duration_seconds': 60
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duration_seconds_max(self):
        """Время выполнения не больше 120 секунд."""
        response = self.client.post('/api/habits/', {
            'place': 'Дом', 'time': '08:00', 'action': 'Тест',
            'duration_seconds': 150
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_related_habit_must_be_pleasant(self):
        """Связанная привычка должна быть приятной."""
        useful = Habit.objects.create(
            user=self.user, place='Улица', time='07:00',
            action='Бег', duration_seconds=60
        )
        response = self.client.post('/api/habits/', {
            'place': 'Дом', 'time': '08:00', 'action': 'Тест',
            'related_habit': useful.id, 'duration_seconds': 60
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pleasant_habit_no_reward_or_related(self):
        """Приятная привычка без вознаграждения и связанной."""
        response = self.client.post('/api/habits/', {
            'place': 'Дом', 'time': '08:00', 'action': 'Тест',
            'is_pleasant': True, 'reward': 'Конфета', 'duration_seconds': 60
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_frequency_range(self):
        """Частота от 1 до 7 дней."""
        response = self.client.post('/api/habits/', {
            'place': 'Дом', 'time': '08:00', 'action': 'Тест',
            'frequency': 10, 'duration_seconds': 60
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HabitAPITest(TestCase):
    """Тесты API привычек."""

    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com', password='Test12345')
        self.other_user = User.objects.create_user(email='other@test.com', password='Test12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user, place='Дом', time='08:00',
            action='Зарядка', duration_seconds=60
        )
        self.public_habit = Habit.objects.create(
            user=self.other_user, place='Парк', time='09:00',
            action='Бег', is_public=True, duration_seconds=60
        )
        self.private_habit = Habit.objects.create(
            user=self.other_user, place='Офис', time='10:00',
            action='Работа', duration_seconds=60
        )

    def test_get_habits_list(self):
        """Получение списка привычек (свои + публичные)."""
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # свой + публичный

    def test_get_public_habits(self):
        """Список публичных привычек."""
        response = self.client.get('/api/habits/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_habit(self):
        """Создание привычки."""
        response = self.client.post('/api/habits/', {
            'place': 'Дом', 'time': '07:00', 'action': 'Йога',
            'duration_seconds': 60
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 4)

    def test_update_own_habit(self):
        """Обновление своей привычки."""
        response = self.client.patch(f'/api/habits/{self.habit.id}/', {
            'action': 'Утренняя зарядка'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, 'Утренняя зарядка')

    def test_update_other_private_habit_denied(self):
        """Нельзя редактировать чужую приватную привычку."""
        response = self.client.patch(f'/api/habits/{self.private_habit.id}/', {
            'action': 'Взлом'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_public_habit_denied(self):
        """Нельзя редактировать чужую публичную привычку."""
        response = self.client.patch(f'/api/habits/{self.public_habit.id}/', {
            'action': 'Взлом'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_habit(self):
        """Удаление своей привычки."""
        response = self.client.delete(f'/api/habits/{self.habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 2)

    def test_delete_other_habit_denied(self):
        """Нельзя удалить чужую привычку."""
        response = self.client.delete(f'/api/habits/{self.private_habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthTest(TestCase):
    """Тесты авторизации."""

    def setUp(self):
        self.user = User.objects.create_user(email='auth@test.com', password='Test12345')
        self.client = APIClient()

    def test_register(self):
        """Регистрация нового пользователя."""
        response = self.client.post('/api/users/register/', {
            'email': 'new@test.com', 'password': 'NewUser12345'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_token(self):
        """Получение JWT токена."""
        response = self.client.post('/api/token/', {
            'email': 'auth@test.com', 'password': 'Test12345'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_access_denied_without_token(self):
        """Без токена доступ запрещён."""
        client = APIClient()
        response = client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PaginationTest(TestCase):
    """Тесты пагинации."""

    def setUp(self):
        self.user = User.objects.create_user(email='page@test.com', password='Test12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        for i in range(7):
            Habit.objects.create(
                user=self.user, place=f'Место {i}', time='08:00',
                action=f'Действие {i}', duration_seconds=60
            )

    def test_pagination_page_size(self):
        """Пагинация по 5 записей."""
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNotNone(response.data['next'])
