# Kursovaya_07


# Проект Django с Celery, PostgreSQL и Redis в Docker

Этот проект представляет собой веб-приложение на Django с использованием Celery для
асинхронных задач, PostgreSQL в качестве базы данных и Redis как брокера сообщений.
Все компоненты работают внутри Docker-контейнеров для упрощения настройки и развертывания.

### Документация по командам

- http://localhost:8000/redoc/
- http://localhost:8000/swagger/

## Структура проекта

- `web`: контейнер с Django-приложением.
- `db`: контейнер базы данных PostgreSQL.
- `redis`: контейнер Redis для брокера сообщений Celery.

## Установка и запуск проекта


```bash
git clone https://github.com/GSmagin/Kursovaya_07.git
cd Kursovaya_07

2. Создайте файл .env
Создайте файл .env в корне проекта и добавьте, заполните параметры из .env.example

3. Запуск контейнеров
Чтобы собрать и запустить контейнеры, выполните команду:

docker-compose up --build
Это команда создаст и запустит контейнеры для Django, PostgreSQL и Redis.

4. Применение миграций
После запуска контейнеров необходимо применить миграции базы данных:

docker-compose exec web python manage.py migrate
5. Создание суперпользователя
Создайте суперпользователя для доступа к административной панели Django:

docker-compose exec web python manage.py createsuperuser
6. Запуск Celery
Для запуска Celery worker и Celery beat выполните следующие команды в отдельных терминалах:

docker-compose exec web celery -A config worker --loglevel=info

docker-compose exec web celery -A config beat --loglevel=info

7. Доступ к приложению
После успешного запуска всех контейнеров приложение будет доступно по адресу http://localhost:8000.

Админка Django доступна по адресу http://localhost:8000/admin.

Полезные команды
Остановка контейнеров:

docker-compose down
Сборка данных в JSON:

docker-compose exec web python manage.py dumpdata > db_backup.json
Восстановление данных из JSON:

docker-compose exec web python manage.py loaddata db_backup.json