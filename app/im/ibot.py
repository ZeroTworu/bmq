from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Awaitable, Callable

if TYPE_CHECKING:
    from app.config.types import BotType


@dataclass
class DtoMessage:
    uid: str
    message: str
    bot_type: 'BotType|None' = None

    def __str__(self):
        return f'<(uid={self.uid}) (message={self.message}) (bot_type={self.bot_type})>'


Callback = Callable[[DtoMessage], Awaitable]


class IBot(metaclass=ABCMeta):
    _type: 'BotType'

    @abstractmethod
    def register_message_callback(self, callback: 'Callback'):
        pass

    @abstractmethod
    async def reply(self, message: 'DtoMessage'):
        pass

    @abstractmethod
    async def build(self):
        pass

    @abstractmethod
    async def destroy(self):
        pass

    @property
    def str_type(self) -> str:
        return str(self._type.value)
