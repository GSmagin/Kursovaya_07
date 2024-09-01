from rest_framework import serializers
from .models import Habit
from django.contrib.auth import get_user_model


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    linked_habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.filter(is_pleasant=True), allow_null=True, required=False)

    class Meta:
        model = Habit
        fields = [
            'id',
            'user',
            'location',
            'time',
            'action',
            'is_pleasant',
            'linked_habit',
            'frequency',
            'reward',
            'duration',
            'is_public',
        ]

    def validate(self, data):
        linked_habit = data.get('linked_habit')
        reward = data.get('reward')
        is_pleasant = data.get('is_pleasant', False)
        duration = data.get('duration', 120)
        frequency = data.get('frequency')

        if linked_habit and reward:
            raise serializers.ValidationError('Нельзя одновременно указывать связанную привычку и вознаграждение.')

        if linked_habit and not linked_habit.is_pleasant:
            raise serializers.ValidationError('Связанная привычка должна быть приятной.')

        if is_pleasant and (reward or linked_habit):
            raise serializers.ValidationError('Приятная привычка не может иметь вознаграждение или связанную привычку.')

        if duration > 120:
            raise serializers.ValidationError('Время на выполнение привычки не должно превышать 120 секунд.')

        if frequency < 1 or frequency > 7:
            raise serializers.ValidationError({'frequency': 'Частота выполнения должна быть от 1 до 7 дней.'})

        return data
