from enum import Enum
from os import getenv


class BotType(Enum):
    TELEGRAM = 'tg'


class CompressorType(Enum):
    GZIP = 'gzip'
    PROTOBUF = 'protobuf'


class AppMode(Enum):
    RECEIVER = 'RECEIVER'
    REPLAYER = 'REPLAYER'


BOT_TYPE = BotType(getenv('BMQ_BOT_TYPE', 'tg').lower())

APP_MODE = AppMode(getenv('BMQ_APP_MODE', 'receiver').upper())

COMPRESSOR_TYPE = CompressorType(getenv('BMQ_COMPRESSOR_TYPE', 'protobuf'))
