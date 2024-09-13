from rest_framework import generics, permissions
from .models import Habit
from .pagination import HabitPagination
from .serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.mixins import LoginRequiredMixin


# Список привычек текущего пользователя с пагинацией
class HabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('id')


# Список публичных привычек
class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by('id')


# Создание привычки
class HabitCreateView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Редактирование привычки
class HabitUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

        # if not self.request.user.is_authenticated:
        #     return Habit.objects.none()  # Возвращаем пустой QuerySet для неавторизованных пользователей
        # return Habit.objects.filter(user=self.request.user)


# Удаление привычки
class HabitDeleteView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

