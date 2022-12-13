from enum import Enum
from os import getenv


class BotType(Enum):
    TELEGRAM = 'tg'
    JABBER = 'jabber'


class CompressorType(Enum):
    GZIP = 'gzip'
    PROTOBUF = 'protobuf'


class AppMode(Enum):
    RECEIVER = 'RECEIVER'
    REPLAYER = 'REPLAYER'


BOT_TYPE_USED = getenv('BMQ_BOT_TYPE_USED', 'tg,jabber').lower()

APP_MODE = AppMode(getenv('BMQ_APP_MODE', 'receiver').upper())

COMPRESSOR_TYPE = CompressorType(getenv('BMQ_COMPRESSOR_TYPE', 'protobuf'))
