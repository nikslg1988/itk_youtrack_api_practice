# N04. Создание задачи в несуществующем проекте

**Тип:** Негативный

**Цель проверки:** Убедиться, что YouTrack отклоняет запрос на создание задачи, если указанного проекта не существует.

### Предусловия

1. YouTrack запущен и доступен.
2. Пользователь авторизован с помощью Permanent Token.
3. Токен действителен.
4. У пользователя есть разрешение Create Issue.
5. Подготовлен идентификатор проекта, которого нет в YouTrack.

### Параметры запроса

| Параметр | Значение |
|---|---|
| HTTP-метод | POST |
| Endpoint | `/api/issues` |
| Authorization | Bearer Token |
| Accept | `application/json` |
| Content-Type | `application/json` |
| fields | `id,idReadable,summary` |
| Request Body | JSON с данными задачи и несуществующим проектом |

**Тестовые данные**

| Поле | Значение |
|---|---|
| summary | API negative test: invalid project |
| description | Issue creation with nonexistent project |
| project.id | `999999-9999` |

**Пример тела запроса:**

```json
{
    "summary": "API negative test: invalid project",
    "description": "Issue creation with nonexistent project",
    "project": {
        "id": "999999-9999"
    }
}
```

### Шаги выполнения

1. Убедиться, что проект с указанным ID отсутствует в YouTrack.
2. Сформировать POST-запрос к endpoint `/api/issues`.
3. Передать действительный токен авторизации в HTTP-заголовке Authorization.
4. Передать заголовки Accept и Content-Type со значением `application/json`.
5. Сформировать JSON-тело запроса с корректным Summary, Description и несуществующим ID проекта.
6. Отправить запрос на сервер.
7. Получить и проверить HTTP-ответ.
8. Проверить, что задача не была создана.

### Ожидаемый результат

1. Сервер возвращает HTTP-статус `400 Bad Request`.
2. Ответ имеет формат JSON.
3. Поле `error` содержит значение `Bad Request`.
4. Поле `error_description` содержит сообщение: `An Project-type entity with the specified ID (999999-9999) was not found`.
5. Поле `error_developer_message` содержит информацию об отсутствии проекта с указанным ID.
6. Задача не создаётся.
7. Существующие задачи и проекты не изменяются.

**Фактическое сообщение об ошибке:**

`An Project-type entity with the specified ID (999999-9999) was not found`

### Постусловия

Состояние YouTrack не изменяется. Новые задачи не создаются.