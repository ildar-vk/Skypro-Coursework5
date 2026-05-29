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
