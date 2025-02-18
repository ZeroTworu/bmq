from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from app.logger import get_logger

if TYPE_CHECKING:
    from logging import Logger
    from typing import Dict

    from app._types import BusCallback


class IBus(metaclass=ABCMeta):
    _logger: 'Logger' = None
    _callbacks: 'Dict[str, BusCallback]' = {}
    _name: str = 'Abstract Message Bus'

    def __init__(self, bus_name: str):
        self._logger = get_logger(bus_name)

    @abstractmethod
    async def publish(self, queue: str, message: bytes):
        pass

    async def register_callback(self, queue_name: str, callback: 'BusCallback'):
        self._callbacks[queue_name] = callback

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def connect(self):
        pass

    @property
    def name(self):
        return self._name
