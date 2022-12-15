from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.im.dto import DtoMessage


class ICompressor(metaclass=ABCMeta):
    _name: str = 'Abstract Compressor'

    @abstractmethod
    async def compress(self, message: 'DtoMessage') -> bytes:
        pass

    @abstractmethod
    async def decompress(self, compressed: bytes) -> 'DtoMessage':
        pass

    @property
    def name(self):
        return self._name
