from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Awaitable, Callable


@dataclass
class DtoMessage:
    uid: int
    message: str

    def __str__(self):
        return f'[(uid={self.uid}) (message={self.message})]'


Callback = Callable[[DtoMessage], Awaitable]


class IBot(metaclass=ABCMeta):

    @abstractmethod
    def register_message_callback(self, callback: 'Callback'):
        pass

    @abstractmethod
    async def reply(self, message: 'DtoMessage'):
        pass

    @abstractmethod
    async def init(self):
        pass

    @abstractmethod
    async def destroy(self):
        pass
