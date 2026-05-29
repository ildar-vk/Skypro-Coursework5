# Atomic Habits Tracker

Трекер полезных привычек по книге Джеймса Клира. Бэкенд на Django REST Framework.

## Технологии
- Python 3.11, Django 4.2, DRF 3.14
- PostgreSQL 15, Redis 7
- Celery, Celery Beat
- Telegram Bot (уведомления)
- JWT авторизация (Simple JWT)
- Gunicorn, Nginx
- Docker, Docker Compose
- GitHub Actions (CI/CD)
- Swagger / Redoc документация

## Локальный запуск (Docker)

```bash
git clone https://github.com/ildar-vk/Skypro-Coursework5.git
cd Skypro-Coursework5
cp .env.template .env  # заполнить реальные значения
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser

## Продакшн-деплой на сервер

```bash
# На сервере:
git clone https://github.com/ildar-vk/Skypro-Coursework5.git
cd Skypro-Coursework5
cp .env.template .env  # заполнить реальные значения
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
API Эндпоинты
МетодURLОписание
POST/api/token/Получить JWT токен
POST/api/token/refresh/Обновить токен
POST/api/users/register/Регистрация
GET/PATCH/api/users/profile/Профиль
GET/POST/api/habits/Список / создать привычку
GET/PATCH/DELETE/api/habits/{id}/Детали / обновить / удалить
GET/api/habits/public/Публичные привычки
Документация API
Swagger: /swagger/

Redoc: /redoc/

CI/CD
GitHub Actions при push в develop или feature/task6:

test — тесты

lint — flake8

build — сборка Docker

deploy — деплой на сервер

Сервер
http://139.100.204.180/admin/
