import gzip
import json

from app.compress.icompress import ICompressor
from app.im.dto import DtoMessage


class GzipCompressor(ICompressor):
    _name: str = 'Gzip Compressor'

    async def compress(self, message: 'DtoMessage') -> bytes:
        dump = json.dumps({'uid': message.uid, 'message': message.message})
        return gzip.compress(bytes(dump, 'utf-8'))

    async def decompress(self, compressed: bytes) -> 'DtoMessage':
        dump = gzip.decompress(compressed).decode('utf-8')
        return DtoMessage(**json.loads(dump))
