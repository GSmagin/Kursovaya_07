from celery import shared_task
from django.utils import timezone
from config import settings
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from .models import Habit
from habits.services import send_telegram_message
from datetime import timedelta
from pytz import timezone as pytz_timezone


@shared_task
def send_reminder():
    # Получаем текущий часовой пояс из настроек Django
    tz = pytz_timezone(settings.TIME_ZONE)

    # Получаем текущее время в этом часовом поясе
    now = timezone.now().astimezone(tz)
    today = now.date()
    current_time = now.time()

    # Округляем текущее время до минут
    rounded_time = current_time.replace(second=0, microsecond=0)

    # Получаем все привычки
    all_habits = Habit.objects.all()
    print(f"All habits: {all_habits}")
    print(f"Current time: {rounded_time}")

    # Фильтрация привычек по времени
    habits_to_check = Habit.objects.filter(time__hour=rounded_time.hour, time__minute=rounded_time.minute)
    print(f"Filtered habits: {habits_to_check}")

    for habit in habits_to_check:
        # Если привычка еще не была выполнена
        last_execution_date = habit.last_execution_date or today - timedelta(days=habit.frequency)
        print(f"Last execution date: {last_execution_date}")

        next_due_date = last_execution_date + timedelta(days=habit.frequency)

        print(f"Last execution date2: {last_execution_date}")
        print(f"Next due date: {next_due_date}")
        print(f"bool: {next_due_date <= today}")

        # Проверяем, наступила ли дата следующего выполнения
        if next_due_date <= today:
            user_profile = habit.user.userprofile
            if user_profile.telegram_chat_id and user_profile.telegram_token:
                if habit.reward:
                    # Если есть вознаграждение
                    message = (f"Напоминание: Время выполнить вашу привычку '{habit.action}'! "
                               f"За выполнение получите вознаграждение '{habit.reward}'!")

                elif habit.linked_habit:
                    # Если есть связанная привычка
                    message = (f"Напоминание: Время выполнить вашу привычку '{habit.action}'! "
                               f"Не забудь выполнить связанную привычку'{habit.linked_habit.action}'!")

                else:
                    message = f"Время выполнить вашу привычку '{habit.action}'!"

                print(f"Sending message to {user_profile.telegram_chat_id}")
                send_telegram_message(user_profile.telegram_token, user_profile.telegram_chat_id, message)
                # Обновляем дату последнего выполнения привычки
                habit.last_execution_date = today
                habit.save()


@shared_task
def send_test_message():

    message = "Это тестовое сообщение от вашего Celery бота!"
    send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)


