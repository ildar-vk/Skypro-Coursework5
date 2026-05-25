from rest_framework.serializers import ValidationError


def validate_habit(data):
    """Валидация привычки согласно бизнес-логике."""

    # 1. Нельзя одновременно reward и related_habit
    if data.get('reward') and data.get('related_habit'):
        raise ValidationError(
            'Выберите что-то одно: вознаграждение или связанную привычку.'
        )

    # 2. Время выполнения ≤ 120 секунд
    duration = data.get('duration_seconds')
    if duration and duration > 120:
        raise ValidationError(
            'Время выполнения привычки не должно превышать 120 секунд.'
        )

    # 3. Связанная привычка должна быть приятной
    related = data.get('related_habit')
    if related and not related.is_pleasant:
        raise ValidationError(
            'Связанная привычка должна быть приятной.'
        )

    # 4. Приятная привычка без вознаграждения и связанной привычки
    if data.get('is_pleasant'):
        if data.get('reward') or data.get('related_habit'):
            raise ValidationError(
                'У приятной привычки не может быть вознаграждения или связанной привычки.'
            )

    # 5. Частота от 1 до 7 дней
    freq = data.get('frequency', 1)
    if freq < 1 or freq > 7:
        raise ValidationError(
            'Частота выполнения должна быть от 1 до 7 дней.'
        )