from django.urls import path
from .views import (
    HabitListView,
    PublicHabitListView,
    HabitCreateView,
    HabitUpdateView,
    HabitDeleteView,
)

urlpatterns = [
    path('habits/', HabitListView.as_view(), name='habit-list'),
    path('habits/public/', PublicHabitListView.as_view(), name='public-habit-list'),
    path('habits/create/', HabitCreateView.as_view(), name='habit-create'),
    path('habits/<int:pk>/update/', HabitUpdateView.as_view(), name='habit-update'),
    path('habits/<int:pk>/delete/', HabitDeleteView.as_view(), name='habit-delete'),
]