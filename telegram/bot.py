import requests
from django.conf import settings


def send_telegram_message(chat_id, text):
    """Отправляет сообщение в Telegram."""
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        return None

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        response = requests.post(url, json={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }, timeout=10)
        return response.json()
    except Exception as e:
        return {'error': str(e)}