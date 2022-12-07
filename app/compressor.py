from abc import ABCMeta, abstractmethod
import gzip
from config.types import COMPRESSOR_TYPE, CompressorType

import json


from app.bot.ibot import DtoMessage


def get_compressor() -> 'ICompressor':
    match COMPRESSOR_TYPE:
        case CompressorType.GZIP:
            return GzipCompressor()
        case _:
            raise ValueError(f'Compressor {COMPRESSOR_TYPE} not supported')


class ICompressor(metaclass=ABCMeta):

    @abstractmethod
    async def compress(self, message: 'DtoMessage') -> bytes:
        pass

    @abstractmethod
    async def decompress(self, compressed: bytes) -> 'DtoMessage':
        pass


class GzipCompressor(ICompressor):

    async def compress(self, message: 'DtoMessage') -> bytes:
        dump = json.dumps({'uid': message.uid, 'message': message.message})
        return gzip.compress(bytes(dump, 'utf-8'))

    async def decompress(self, compressed: bytes) -> 'DtoMessage':
        dump = gzip.decompress(compressed).decode('utf-8')
        return DtoMessage(**json.loads(dump))
