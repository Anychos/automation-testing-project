# Автоматизация тестирования веб-приложения

Учебный проект по автоматизации тестирования веб-приложения. Цель проекта — освоить построение поддерживаемого автотестового фреймворка на Python: от API-клиентов и моделей данных до фикстур, проверок и тестовых сценариев.

## Текущий статус

Проект находится в работе. Реализован набор API-автотестов для учебного приложения BookingLab.

## Проверяемые сущности

API-тесты проверяют:

- регистрацию и вход, включая неверные данные и границы длины пароля;
- получение текущего пользователя и проверку доступа без токена или с неверным токеном;
- создание, получение, изменение и отключение комнат, а также отдельные негативные сценарии;
- создание, получение, отмену бронирований и принятие оплаты в обработку;
- доступность сервиса (`health`).

Для тестов используются API-клиенты, Pydantic-схемы, фикстуры, генератор тестовых данных и переиспользуемые проверки ответов.

## Структура проекта

```text
.
├── src/api/
│   ├── assertions/  # Переиспользуемые проверки API-ответов
│   ├── clients/     # Базовый и специализированные HTTP-клиенты
│   ├── fixtures/    # Pytest-фикстуры
│   ├── schemas/     # Pydantic-модели запросов и ответов
│   └── tools/       # Маршруты и генерация тестовых данных
├── tests/api/       # API-автотесты
├── conftest.py      # Общие настройки pytest
├── pytest.ini       # Конфигурация pytest
└── requirements.txt # Зависимости проекта
```

## Технологии

- Python 3.14 (проверенная версия);
- pytest;
- httpx;
- Pydantic;
- Faker.

## Первый запуск

Проект проверялся на Windows с Python 3.14. Для изолированной установки:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`pydantic-settings` нужен для загрузки настроек из `config.py`. `tzdata`
поставляется явно: на Windows он предоставляет IANA-данные для
`ZoneInfo("Europe/Moscow")`, используемого генератором тестовых данных.

Запустите [BookingLab](https://github.com/Anychos/automation-testing-project-base-app) по инструкции в его README и создайте начальные данные командой `seed`. В репозитории автотестов самого приложения нет.

Создайте локальный `.env` на основе `.env.example`. Укажите адрес API с суффиксом `/api`, например `http://localhost:8000/api`, таймаут и учётные данные администратора и пользователя из `.env` приложения:

```dotenv
CLIENT_SETTINGS.BASE_URL=http://localhost:8000/api
CLIENT_SETTINGS.TIMEOUT=10
ADMIN_DATA.EMAIL=<SEED_ADMIN_EMAIL>
ADMIN_DATA.PASSWORD=<SEED_ADMIN_PASSWORD>
USER_DATA_SESSION.EMAIL=<SEED_USER_EMAIL>
USER_DATA_SESSION.PASSWORD=<SEED_USER_PASSWORD>
```

Подставьте реальные значения из локального `.env` приложения. Перед тестами pytest проверяет готовность API через `/health/ready`.

Проверки стиля используют системные команды `ruff` и `pre-commit`, поэтому
установите их в активное окружение и зарегистрируйте hooks:

```powershell
python -m pip install ruff pre-commit
pre-commit install
ruff check --no-cache --select E4,E7,E9,F,I .
ruff format --no-cache --check .
```

## Запуск тестов

Команды выполняются из корня проекта автотестов при запущенном API:

```powershell
python -m pytest -q tests/api                # все API-тесты
python -m pytest -q tests/api -m smoke       # короткий набор
python -m pytest -q tests/api -m regression  # полный регрессионный набор
python -m pytest --collect-only -q            # проверить сбор тестов
```

Тесты создают пользователей, комнаты и бронирования на стенде. Для восстановления начальных тестовых данных после завершения тестов и обработки платежей можно выполнить:

```powershell
python tests/reset_test_data.py
```

Скрипт использует учётную запись ADMIN из `.env`, удаляет данные тестового стенда и восстанавливает начальные данные. API разрешает эту операцию только при `TEST_MODE=true` и `APP_ENV=development` или `test`. После сброса старые токены недействительны; данные Kafka и отдельного payment-service не очищаются.

## CI

При push GitHub Actions запускает workflow `.github/workflows/api-tests.yml`: он получает зафиксированную версию BookingLab, запускает backend и базу через Docker Compose, создаёт начальные данные и выполняет все API-тесты.

## Планы развития

- расширить API-покрытие для пользователей, комнат и бронирований;
- добавить позитивные, негативные и граничные сценарии;
- внедрить UI-автоматизацию веб-приложения;
- добавить отчётность.
