import requests

from config.settings import TELEGRAM_URL


def send_telegram_message(token, chat_id, message):
    params = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(TELEGRAM_URL + token + '/sendMessage', params)
