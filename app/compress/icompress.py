from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.im.ibot import DtoMessage


class ICompressor(metaclass=ABCMeta):

    @abstractmethod
    async def compress(self, message: 'DtoMessage') -> bytes:
        pass

    @abstractmethod
    async def decompress(self, compressed: bytes) -> 'DtoMessage':
        pass
