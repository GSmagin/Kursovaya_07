# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код проекта в контейнер
COPY . .

# Устанавливаем переменные окружения для Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Добавляем пользователя для безопасного запуска
RUN adduser --disabled-password myuser
USER myuser

# Команда по умолчанию
CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]