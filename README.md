# TenderHelp

Проверка ИНН или ОГРН в [реестре субъектов МСП](https://rmsp.nalog.ru/). Можно посмотреть историю прошлых проверок; повторный запрос в течение 5 минут отдаётся из кэша.

## Запуск

Нужен Docker Desktop.

```bash
docker compose up --build
```

После старта:

- приложение — http://localhost:8080  
- API / Swagger — http://localhost:8001/docs  

Остановить:

```bash
docker compose down
```

Для проверки удобно взять ИНН `4707048043` (есть в реестре). Крупные компании вроде Сбера в реестре МСП обычно не числятся — это нормально.

## Стек

- **Backend:** FastAPI, Postgres, Redis, Kafka  
- **Frontend:** Vue 3, TypeScript, Quasar  
- Всё поднимается через `docker compose`
