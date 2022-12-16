from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app._types import BotType, DtoMessage, MessageCallback


class IBot(metaclass=ABCMeta):
    _type: 'BotType'

    @abstractmethod
    def register_message_callback(self, callback: 'MessageCallback'):
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
