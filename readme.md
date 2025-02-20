# Referral API Service

Это `API` для работы с реферальной системой.

## Технологии

- Python 3.12
- Redis
- SQLAlchemy
- PostgreSQL
- Внешний API: emailhunter.co
- Docker

## Структура проекта

```plaintext
.
├── app/
│   ├── api/                   # Внешние API
│   │   ├── __init__.py
│   │   ├── exceptions.py      # Ошибки связанные с внешним API
│   │   ├── service.py         # Логика работы c API
│   ├── auth/                  # Логика аутентификации и регистрации
│   │   ├── __init__.py
│   │   ├── handlers.py        # Обработчики запросов
│   │   ├── service.py         # Сервисы для работы с авторизацией
│   │   ├── schemas.py         # Схемы данных для авторизации
│   │   ├── exceptions.py      # Ошибки связанные с авторизацией
│   │   ├── utils.py           # Хеширование паролей
│   ├── cache/                 # Кеш (Redis)
│   │   ├── __init__.py
│   │   ├── connection.py      # Создание соединения с Redis
│   │   ├── service.py         # Логика работы с Redis
│   ├── database/              # Работа с БД
│   │   ├── __init__.py
│   │   ├── session.py         # Настройки сессии для SQLAlchemy
│   │   ├── base.py            # Базовый класс Моделей
│   ├── referral/              # Логика работы с рефералами
│   │   ├── __init__.py
│   │   ├── exceptions.py      # Ошибки связанные с авторизацией
│   │   ├── handlers.py        # Обработчики запросов 
│   │   ├── service.py         # Логика работы с рефералами
│   │   ├── schemas.py         # Схемы данных для рефералов
│   ├── users/                 # Пользователи
│   │   ├── __init__.py
│   │   ├── exceptions.py      # Ошибки связанные с пользователями
│   │   ├── handlers.py        # Обработчики запросов 
│   │   ├── service.py         # Логика работы с пользователями
│   │   ├── schemas.py         # Схемы данных для работы с пользователями
│   │   ├── repository.py      # Репозиторий
│   ├── __init__.py
│   ├── settings.py            # Файл настроек проекта
│   ├── main.py                # Основной файл приложения
│   ├── exceptions.py          # Файл с обьялвенным классм ApplicationException
│   ├── dependency.py          # Зависимости проекта
├── alembic/                   # Миграции базы данных
├── Dockerfile                 # Docker образ приложения
├── docker_compose.yaml        # Docker-Compose
├── pyproject.toml             # Зависимости
└── README.md                  # Описание проекта


```

## Инструкция по установке

1. Установите зависимости:

```bash
poetry install
```

2. Инициализируйте базу данных:

```bash
poetry run alembic init /migrations
```

3. Обновить путь в `alembic.ini`

```file
sqlalchemy.url =  postgresql://postgres:root@db:5432/referral_db
```

4.Импортирвать модели в `migrations/env.py`

```python
# for 'autogenerate' support
from app.users.models import User
from app.database.base import Base

target_metadata = Base.metadata
```
5. Выполните первичную миграцию 

```bash
alembic revision --autogenerate -m "Init migration"`
``` 
6.Запустите приложение с Docker:

```bash
docker compose up -d
```

## Внешние API

`emailhunter.co` — используется для валидации email-адресов при регистрации пользователей и рефереров.

Подключение реализуется через `HunterApiService`, используя библиотеку `httpx`.

Примерный ответ от `API`:

```json
{
  "data": {
    "status": "disposable",
    "result": "risky",
    "_deprecation_notice": "Using result is deprecated, use status instead",
    "score": 0,
    "email": "test@example.com",
    "regexp": true,
    "gibberish": false,
    "disposable": true,
    "webmail": false,
    "mx_records": false,
    "smtp_server": false,
    "smtp_check": false,
    "accept_all": false,
    "block": false,
    "sources": []
  },
  "meta": {
    "params": {
      "email": "test@example.com"
    }
  }
}

```
