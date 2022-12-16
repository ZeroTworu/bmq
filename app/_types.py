from dataclasses import dataclass
from enum import Enum
from typing import Awaitable, Callable


@dataclass
class DtoMessage:
    uid: str
    message: str
    bot_type: 'BotType|None' = None

    def __str__(self):
        return f'<(uid={self.uid}) (message={self.message}) (bot_type={self.bot_type})>'


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
