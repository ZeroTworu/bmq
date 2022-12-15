from os import getenv

from app._types import AppType, BusType, CompressorType

BOT_TYPE_USED = getenv('BMQ_BOT_TYPE_USED', 'tg,jabber').lower()

APP_MODE = AppType(getenv('BMQ_APP_MODE', 'receiver').upper())

COMPRESSOR_TYPE = CompressorType(getenv('BMQ_COMPRESSOR_TYPE', 'protobuf'))

BUS_TYPE = BusType(getenv('BMQ_BUS_TYPE', 'redis'))
