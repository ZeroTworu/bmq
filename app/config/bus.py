from os import getenv

from app._types import BusType

RMQ_DSN = getenv('BMQ_RMQ_DSN', 'amqp://user:password@127.0.0.1/')

REDIS_DSN = getenv('BMQ_REDIS_DSN', 'redis://localhost/')

BUS_TYPE = BusType(getenv('BMQ_BUS_TYPE', 'redis'))
