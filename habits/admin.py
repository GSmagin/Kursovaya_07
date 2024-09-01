from django.contrib import admin
from .models import Habit


class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'time', 'action', 'is_pleasant', 'linked_habit', 'frequency', 'reward', 'duration', 'is_public')
    list_filter = ('is_pleasant', 'is_public', 'frequency')
    search_fields = ('action', 'reward', 'location')
    ordering = ('-time',)


admin.site.register(Habit, HabitAdmin)
