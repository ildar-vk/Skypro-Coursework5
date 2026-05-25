from celery import shared_task
from django.utils import timezone
from .models import Habit
from telegram.bot import send_telegram_message


@shared_task(name='habits.tasks.send_habit_reminders')
def send_habit_reminders():
    """Проверяет привычки и отправляет напоминания в Telegram."""
    now = timezone.localtime().time()
    habits = Habit.objects.filter(is_pleasant=False).select_related('user', 'related_habit')

    for habit in habits:
        if habit.time.hour == now.hour and habit.time.minute == now.minute:
            chat_id = getattr(habit.user, 'telegram_chat_id', None)
            if not chat_id:
                continue

            message = (
                f'🔔 <b>Напоминание о привычке</b>\n\n'
                f'<i>{habit.action}</i>\n'
                f'📍 <b>Место:</b> {habit.place}\n'
                f'⏰ <b>Время:</b> {habit.time.strftime("%H:%M")}\n'
            )

            if habit.reward:
                message += f'🏆 <b>Вознаграждение:</b> {habit.reward}'
            elif habit.related_habit:
                message += f'🎯 <b>Затем:</b> {habit.related_habit.action}'

            send_telegram_message(chat_id, message)