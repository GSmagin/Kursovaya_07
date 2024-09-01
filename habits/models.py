from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from utils.const import NULLABLE
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits',
                             verbose_name=_('user'))
    location = models.CharField(max_length=255, **NULLABLE,  verbose_name=_('Место'))
    time = models.TimeField(verbose_name=_('Время'))
    action = models.CharField(max_length=255, verbose_name=_('Действие'))
    is_pleasant = models.BooleanField(default=False, verbose_name=_('Признак приятной привычки'))
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE,
                                     related_name='linked_to', verbose_name=_('Связанная привычка'))
    frequency = models.PositiveIntegerField(default=1, verbose_name=_('Периодичность дней'))  # Количество дней между повторениями
    reward = models.CharField(max_length=255, **NULLABLE, verbose_name=_('Вознаграждение'))
    duration = models.PositiveIntegerField(default=120,  verbose_name=_('Время на выполнение (seconds)'))  # Время в секундах
    is_public = models.BooleanField(default=False, verbose_name=_('Признак публичности'))
    last_execution_date = models.DateField(**NULLABLE, verbose_name=_('Дата последнего выполнения'))

    def clean(self):
        # Проверка одновременного заполнения linked_habit и reward
        if self.linked_habit and self.reward:
            raise ValidationError('Нельзя одновременно указывать связанную привычку и вознаграждение.')

        # Проверка, что linked_habit является приятной
        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError('Связанная привычка должна быть приятной.')

        # Проверка, что приятная привычка не имеет reward или linked_habit
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError('Приятная привычка не может иметь вознаграждение или связанную привычку.')

        # Проверка времени выполнения
        if self.duration > 120:
            raise ValidationError('Время на выполнение привычки не должно превышать 120 секунд.')

        # Проверка частоты выполнения
        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError('Частота выполнения должна быть от 1 до 7 дней.')


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('habit')
        verbose_name_plural = _('habits')

    def __str__(self):
        return f"{self.action} at {self.time} in {self.location or 'anywhere'}"

