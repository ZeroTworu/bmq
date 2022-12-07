### BMQ - Bot for MQ

### Requirements

1. Python >= 3.10
2. Docker, docker-compose

### Быстрый запуск

Запускает инфраструктуру, собирает приложение, поднимает сервисы `receiver` и `replayer`

1. Скопировать файл `docker/docker-compose.app.yaml.example` в `docker/docker-compose.app.yaml`
2. Отредактировать в нём параметры необходимые для подключения, согласно таблицей ниже.
3. Выполнить `make app`

## Локальный запуск вне контейнера.

### Установка зависимостей

1. `make install-deps`
2. Выставить переменные окружения согласно таблице ниже.
3. `make local`

### Описание переменных окружения

| ENV                   | Описание                                          | required | default                         |
|-----------------------|---------------------------------------------------|----------|---------------------------------|
| BMQ_TG_API_ID         | Telegram API ID                                   | +        |                                 |
| BMQ_TG_API_HASH       | Telegram API hash                                 | +        |                                 |
| BMQ_TG_BOT_TOKEN      | Telegram API token                                | +        |                                 |
| BMQ_RMQ_DSN           | Строка подключения к RMQ                          | -        | amqp://user:password@127.0.0.1/ |
| BMQ_RMQ_ROUTING_KEY   | RMQ routing key                                   | -        | bmq                             |
| BMQ_RMQ_QUEUE         | Очередь сообщений                                 | -        | bmq                             |
| BMQ_BOT_TYPE          | Тип используемого бота, пока только Telegram      | -        | tg                              |
| BMQ_APP_MODE          | Режим работы приложения `receiver` или `replayer` | -        | receiver                        |
| BMQ_COMPRESSOR_TYPE   | Тип сжатия сообщений, только `gzip`               | -        | gzip                            |


