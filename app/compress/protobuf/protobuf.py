from app.compress.icompress import ICompressor
from app.compress.protobuf.proto import message_pb2 as pb_message
from app.im.dto import DtoMessage


class ProtobufCompressor(ICompressor):

    _name: str = 'Protobuf Compressor'

    async def compress(self, message: 'DtoMessage') -> bytes:
        msg = pb_message.Message()
        msg.uid = message.uid
        msg.message = message.message
        return msg.SerializeToString()

    async def decompress(self, compressed: bytes) -> 'DtoMessage':
        msg = pb_message.Message()
        msg.ParseFromString(compressed)
        return DtoMessage(uid=msg.uid, message=msg.message)
