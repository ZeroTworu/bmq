from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Awaitable, Callable


@dataclass
class DtoMessage:
    uid: int
    message: str


Callback = Callable[[DtoMessage], Awaitable]


class IBot(metaclass=ABCMeta):

    @abstractmethod
    def register_message_callback(self, callback: 'Callback'):
        pass

    @abstractmethod
    async def reply(self, message: str):
        pass

    @abstractmethod
    async def init(self):
        pass
