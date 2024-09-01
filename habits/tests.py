from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase

from habits.models import Habit
from django.contrib.auth import get_user_model
from datetime import time
from rest_framework import status
from django.urls import reverse

from habits.serializers import HabitSerializer

User = get_user_model()


class HabitModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')

    def test_create_habit_with_valid_data(self):
        habit = Habit.objects.create(
            user=self.user,
            location='Дом',
            time=time(9, 0),
            action='Утренняя зарядка',
            frequency=1,
            duration=120
        )
        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.location, 'Дом')
        self.assertEqual(habit.time, time(9, 0))
        self.assertEqual(habit.action, 'Утренняя зарядка')
        self.assertEqual(habit.frequency, 1)
        self.assertEqual(habit.duration, 120)

    def test_habit_invalid_linked_habit_and_reward(self):
        linked_habit = Habit.objects.create(
            user=self.user,
            location='Офис',
            time=time(14, 0),
            action='Пить воду',
            is_pleasant=True
        )
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                location='Дом',
                time=time(9, 0),
                action='Утренняя зарядка',
                linked_habit=linked_habit,
                reward='Чашка кофе'
            )
            habit.full_clean()

    def test_habit_invalid_linked_habit_not_pleasant(self):
        linked_habit = Habit.objects.create(
            user=self.user,
            location='Офис',
            time=time(14, 0),
            action='Пить воду',
            is_pleasant=False
        )
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                location='Дом',
                time=time(9, 0),
                action='Утренняя зарядка',
                linked_habit=linked_habit
            )
            habit.full_clean()

    def test_habit_invalid_duration(self):
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                location='Дом',
                time=time(9, 0),
                action='Утренняя зарядка',
                duration=130  # Invalid duration, more than 120 seconds
            )
            habit.full_clean()

    def test_habit_invalid_frequency(self):
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                location='Дом',
                time=time(9, 0),
                action='Утренняя зарядка',
                frequency=8  # Invalid frequency, more than 7 days
            )
            habit.full_clean()


class HabitSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')

    def test_valid_serializer(self):
        data = {
            'user': self.user.email,
            'location': 'Дом',
            'time': time(9, 0),
            'action': 'Утренняя зарядка',
            'frequency': 1,
            'duration': 120
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_linked_habit_and_reward(self):
        linked_habit = Habit.objects.create(
            user=self.user,
            location='Офис',
            time=time(14, 0),
            action='Пить воду',
            is_pleasant=True
        )
        data = {
            'user': self.user.email,
            'location': 'Дом',
            'time': time(9, 0),
            'action': 'Утренняя зарядка',
            'linked_habit': linked_habit.pk,
            'reward': 'Чашка кофе'
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'non_field_errors'})

    def test_invalid_serializer_duration(self):
        data = {
            'user': self.user.email,
            'location': 'Дом',
            'time': time(9, 0),
            'action': 'Утренняя зарядка',
            'duration': 130  # Invalid duration
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertIn('Время на выполнение привычки не должно превышать 120 секунд.',
                      serializer.errors['non_field_errors'])

    def test_invalid_serializer_frequency(self):
        data = {
            'user': self.user.email,
            'location': 'Офис',
            'time': time(9, 0),
            'action': 'Ежедневная встреча',
            'frequency': 0  # Недопустимое значение для частоты
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())  # Ожидается, что данные будут недействительными
        self.assertIn('frequency', serializer.errors)
        self.assertIn('Частота выполнения должна быть от 1 до 7 дней.', serializer.errors['frequency'])


class HabitAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)  # Используйте force_authenticate для аутентификации
        self.habit = Habit.objects.create(
            user=self.user,
            location='Дом',
            time=time(9, 0),
            action='Утренняя зарядка',
            frequency=1,
            duration=120
        )

    def test_get_habit_list(self):
        url = reverse('habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_habit(self):
        url = reverse('habit-create')
        data = {
            'location': 'Офис',
            'time': '14:00:00',  # Формат времени как строка
            'action': 'Пить воду',
            'frequency': 1,
            'duration': 120
        }
        response = self.client.post(url, data, format='json')  # Указывайте format='json'
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_update_habit(self):
        url = reverse('habit-update', kwargs={'pk': self.habit.pk})
        data = {
            'location': 'Офис',
            'time': '14:00:00',  # Формат времени как строка
            'action': 'Пить воду',
            'frequency': 1,
            'duration': 120
        }
        response = self.client.put(url, data, format='json')  # Указывайте format='json'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.location, 'Офис')

    def test_delete_habit(self):
        url = reverse('habit-delete', kwargs={'pk': self.habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_get_public_habit_list(self):
        public_habit = Habit.objects.create(
            user=self.user,
            location='Парк',
            time=time(18, 0),
            action='Вечерняя пробежка',
            is_public=True,
            frequency=1,
            duration=120
        )
        url = reverse('public-habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['action'], 'Вечерняя пробежка')