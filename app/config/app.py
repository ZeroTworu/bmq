from os import getenv

from app._types import AppType, CompressorType

BOT_TYPE_USED = getenv('BMQ_BOT_TYPE_USED', 'tg,jabber').lower()

APP_MODE = AppType(getenv('BMQ_APP_MODE', 'receiver').upper())

COMPRESSOR_TYPE = CompressorType(getenv('BMQ_COMPRESSOR_TYPE', 'protobuf'))

IDLE_TIMEOUT = float(getenv('BMQ_IDLE_TIMEOUT', 1))
