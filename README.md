# DNF_V3

Учебный проект для практики работы с FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker и тестированием API.

Продолжение практики и улучшение навыков после:

- https://github.com/Osnowa/Docker_Ngnix_FastAPI_V2.git
- https://github.com/Osnowa/Docker_Ngnix_FastAPI.git

## Стек

- FastAPI
- SQLAlchemy Async
- PostgreSQL
- Alembic
- Docker / Docker Compose
- Nginx
- Pytest
- HTTPX

## Улучшения проекта

- Добавлено логирование с помощью `logging`
- Добавлен `.env` для хранения настроек и секретов
- Добавлен `.env.example` с примером необходимых переменных
- Реализован CRUD для работы со словами
- Добавлено разделение приложения на роутеры, модели, схемы и репозитории

## Docker

- PostgreSQL запускается в отдельном контейнере
- Nginx используется как reverse proxy
- Docker Compose разделён на конфигурации для production и development
- Для разработки используется bind mount и `--reload`
- Создан `Makefile` для удобного запуска проекта

## База данных

- PostgreSQL используется как основная база данных
- SQLAlchemy используется в асинхронном режиме
- Alembic отвечает за создание и изменение структуры таблиц
- Реализована работа с connection pool

## Тестирование

- Добавлены интеграционные тесты API
- Используется `pytest` + `httpx.AsyncClient`
- Для тестов используется отдельная SQLite БД
- SQLite используется как реальная тестовая БД, а не `:memory:`
- Через `dependency_overrides` тесты получают тестовую БД вместо основной
- Созданы фикстуры для управления тестовой БД и предварительного заполнения данными

## Реализованные endpoints

- `GET /words/` — получить все слова
- `GET /words/{id}` — получить слово
- `POST /words/` — добавить слово
- `PATCH /words/{id}` — изменить слово
- `DELETE /words/{id}` — удалить слово
- `DELETE /words/` — удалить все слова