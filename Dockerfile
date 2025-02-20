# Используем официальный образ Python в качестве базового
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /app/

# Копируем файлы проекта
COPY . /app/

# Устанавливаем Poetry


# Устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root


# Открываем порт для приложения
EXPOSE 8000

# Запускаем миграции и стартуем сервер
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
