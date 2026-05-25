from django.db import models
from django.conf import settings


class Habit(models.Model):
    FREQUENCY_CHOICES = [(i, f'Раз в {i} дн.') for i in range(1, 8)]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'is_pleasant': True},
        verbose_name='Связанная привычка'
    )
    frequency = models.PositiveSmallIntegerField(
        default=1,
        choices=FREQUENCY_CHOICES,
        verbose_name='Периодичность (дни)'
    )
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вознаграждение')
    duration_seconds = models.PositiveIntegerField(default=120, verbose_name='Длительность (сек)')
    is_public = models.BooleanField(default=False, verbose_name='Публичная')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['time']
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'{"😊" if self.is_pleasant else "⚡"} {self.action} в {self.place} в {self.time}'
