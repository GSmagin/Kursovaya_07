from celery import shared_task
from django.utils import timezone
from config import settings
from .models import Habit
from telegram import Bot
from telegram.error import TelegramError
import asyncio


@shared_task
def send_reminder():
    now = timezone.now()
    today = now.date()
    current_time = now.time()

    # Получаем все привычки, которые должны быть выполнены сегодня
    habits = Habit.objects.filter(time=current_time, frequency__lte=7)

    def send_message_to_user(token, chat_id, message):
        bot = Bot(token=token)
        try:
            bot.send_message(chat_id=chat_id, text=message)
            print(f"Message sent: {message}")
        except TelegramError as e:
            print(f"An error occurred while sending message: {e}")

    for habit in habits:
        user_profile = habit.user.userprofile
        if user_profile.telegram_chat_id and user_profile.telegram_token:
            message = f"Напоминание: Время выполнить вашу привычку '{habit.action}'!"
            # Отправка сообщения синхронно
            send_message_to_user(user_profile.telegram_token, user_profile.telegram_chat_id, message)



