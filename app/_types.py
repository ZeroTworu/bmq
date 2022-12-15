from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Awaitable, Callable

    from app.im.dto import DtoMessage

    MessageCallback = Callable[[DtoMessage], Awaitable]
    BusCallback = Callable[[bytes], Awaitable]


class BusType(Enum):
    RMQ = 'rmq'
    REDIS = 'redis'


class BotType(Enum):
    TELEGRAM = 'tg'
    JABBER = 'jabber'


class CompressorType(Enum):
    GZIP = 'gzip'
    PROTOBUF = 'protobuf'


class AppType(Enum):
    RECEIVER = 'RECEIVER'
    REPLAYER = 'REPLAYER'
