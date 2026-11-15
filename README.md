# ITK YouTrack API Tests

API-тесты YouTrack Server на Python, Requests и Pytest.

## Стек

- Python 3.14+
- Requests, Pytest, Pydantic
- pytest-xdist, pytest-html
- uv, Docker Compose, Ruff

## Запуск YouTrack

Перед запуском проверь пути к каталогам данных в `docker-compose.yml`: сейчас там указаны абсолютные пути конкретной машины.

```bash
docker compose up -d
```

После первого запуска открой `http://localhost:8080`, заверши настройку YouTrack и создай Permanent Token для тестового пользователя.

## Настройка проекта

Установи зависимости:

```bash
uv sync
```

Создай `.env` в корне проекта:

```dotenv
YOUTRACK_BASE_URL=http://localhost:8080
YOUTRACK_TOKEN=perm:YOUR_PERMANENT_TOKEN
```

Не добавляй `.env` в Git.

## Запуск тестов

Все тесты:

```bash
uv run python -m pytest -v -s
```

Параллельный запуск:

```bash
uv run python -m pytest -v -s -n auto
```

HTML-отчёт:

```bash
uv run python -m pytest -v -s -n auto --html=reports/report.html --self-contained-html
```

Открой `reports/report.html` в браузере. Убедись, что `/reports/` указан в `.gitignore`.

## Тестовые сценарии

**Позитивные:** получение списка задач, получение задачи по ID, создание и обновление задачи, добавление комментария.

**Негативные:** получение несуществующей задачи, создание задачи без названия, запрос с недействительным токеном, создание задачи с несуществующим проектом, добавление пустого комментария.

Тест-кейсы описаны в `docs/test-cases/`. Тесты используют Pydantic-модели из `schemas/`. Для проверки несуществующих проектов применяется параметризация Pytest с тремя значениями `project_id`.

## Структура

```text
client/       HTTP-клиент YouTrack
schemas/      Pydantic-модели
tests/        API-тесты и фикстуры
docs/         Описания тест-кейсов
```

## Проверка кода

```bash
uv run ruff check .
uv run ruff format --check .
```
