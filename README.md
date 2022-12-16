### BMQ

Echo microservice multi protocol bot.

Состоит из двух сервисов: `receiver` и `replayer`, связь между сервисами осуществляется через RMQ.

Поддерживает одновременную работу через `Telegram` и `Jabber`.

Поддерживает две шины для обмена данными между сервисами - `RabbitMQ` и `Redis`.

#### `Receiver`

Сервис принимающий сообщения от пользователя и отправляющий сообщение в шину данных.

#### `Replayer`

Сервис принимающий сообщения из шины данных и отправляющий их обратно пользователю.

### Requirements

1. Python >= 3.10.
2. Docker, docker-compose.

### Быстрый запуск

Запускает инфраструктуру, собирает приложение, поднимает сервисы `receiver` и `replayer`.

1. Скопировать файл `docker/docker-compose.app.yaml.example` в `docker/docker-compose.app.yaml`.
2. Отредактировать в нём параметры необходимые для подключения, согласно [таблице](#Описание-переменных-окружения) ниже.
3. Выполнить `make app`

## Локальный запуск вне контейнера.

### Установка зависимостей

1. `make install-deps`.
2. Выставить переменные окружения согласно [таблице](#Описание-переменных-окружения) ниже.
3. `make infra` - поднятие RMQ.
4. `make local` или `poetry run python -m app`.

### Описание переменных окружения
* `~` - означает что переменная должна быть заполнена в зависимости от выбора используемых ботов.

| ENV                 | Description                                                                        | Required | Default                           |
|---------------------|------------------------------------------------------------------------------------|----------|-----------------------------------|
| BMQ_TG_API_ID       | Telegram API ID                                                                    | ~        |                                   |
| BMQ_TG_API_HASH     | Telegram API hash                                                                  | ~        |                                   |
| BMQ_TG_BOT_TOKEN    | Telegram API token                                                                 | ~        |                                   |
| BMQ_JABBER_UID      | Jabber UID                                                                         | ~        |                                   |
| BMQ_JABBER_PASSWORD | Jabber password                                                                    | ~        |                                   |
| BMQ_RMQ_DSN         | Строка подключения к RMQ                                                           | -        | `amqp://user:password@127.0.0.1/` |
| BMQ_REDIS_DSN       | Строка подключения к Redis                                                         | -        | `redis://localhost/`              |
| BMQ_BOT_TYPE_USED   | Тип используемых ботов, через `,`, `tg` для Telegram `jabber` для Jabber           | -        | `tg,jabber`                       |
| BMQ_APP_MODE        | Режим работы приложения `receiver` или `replayer`                                  | -        | `receiver `                       |
| BMQ_COMPRESSOR_TYPE | Тип сжатия сообщений, `gzip` или `protobuf`                                        | -        | `protobuf`                        |
| BMQ_IDLE_TIMEOUT    | Время простоя главного цикла в секундах                                            | -        | `1`                               |
| BMQ_LOG_LEVEL       | Уровень логирования                                                                | -        | `INFO`                            |
| BMQ_BUS_TYPE        | Тип шины обмена данными `rmq` или `redis`. `rmq` - для RabbitMQ, `redis` для Redis | -        | `rmq`                             |

### Запуск линтера
`make lint`

### Генерация protobuf
`make proto`

### Структура проекта
1. `app.bus` - Шина обмена данными между микросервисами.
   1. `app.bus.IBus` - Интерфейс шины обмена данными.
   2. `app.bus.RabbitMqBus` - Реализация шины, для обмена через `RabbitMQ`
   3. `app.bus.RedisBus` - Реализация шины, для обмена через `Redis`

2. `app.compress` - Реализация сжатия сообщений.
   1. `app.compress.ICompressor` - Интерфейс описывающий компрессор сообщений.
   2. `capp.ompress.GzipCompressor` - Реализация сжатия через `Gzip`. 
   Сжимает `JSON` строку в которую преобразуется `_types.DtoMessage`
   3. `app.compress.ProtobufCompressor` - Реализация сжатия через `protobuf`.
   Генерится из `proto.message.proto` через `make proto`

3. `app.config` - Конфигурация приложения загружаемая из `ENV`
4. `app.domain` - Основное приложение.
   1. `app.domain.manager.Manager` - Менеджер микросоервисов, отвечает за запуск в зависимости от `config.app.APP_MODE`, останов, и main Idle.
   2. `app.domain,services.IService` - Абстрактный класс, описывающий сервис.
   3. `app.domain.servicers.ReceiverService` - Сервис принимающий сообщения из im и передающий их в `replayer`
   4. `app.domain.servicers.ReplayerService` - Принимает сообщения от `receiver` через шину, и отправляет обратно в im.
5. `app.im` - Реализация ботов для im.
   1. `app.im.IBot` - Интерфейс бота, бот должен уметь регистрировать callback на сообщение `register_message_callback` и
   отвечать `reply`. Методы `build` и `destroy` предназначены для инициализации / завершения, и имеют такие названия, что бы не пересекаться со стандартными `start` / `stop`.
   2. `app.im.TelegramBot` - Реализация работы с Telegram im.
   3. `app.im.JabberBot` - Реализация работы с Jabber im.
6. `app._types` - Описание кастомных типов приложения, `_` в названии, нужна для корректной рабоды debug в Pycharm.
