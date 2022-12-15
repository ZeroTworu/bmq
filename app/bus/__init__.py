from typing import TYPE_CHECKING

from app._types import BusType
from app.bus.redis import RedisBus
from app.bus.rmq import RabbitMqBus
from app.config.app import BUS_TYPE

if TYPE_CHECKING:
    from app.bus.ibus import IBus


def get_bus() -> 'IBus':
    match BUS_TYPE:
        case BusType.RMQ:
            return RabbitMqBus()
        case BusType.REDIS:
            return RedisBus()
        case _:
            raise ValueError(f'Unknown bus type {BUS_TYPE}')
