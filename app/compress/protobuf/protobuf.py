from app.bot.ibot import DtoMessage
from app.compress.icompress import ICompressor
from app.compress.protobuf import message_pb2 as pb_message


class ProtobufCompressor(ICompressor):

    async def compress(self, message: 'DtoMessage') -> bytes:
        msg = pb_message.Message()
        msg.uid = message.uid
        msg.message = message.message
        return msg.SerializeToString()

    async def decompress(self, compressed: bytes) -> 'DtoMessage':
        msg = pb_message.Message()
        msg.ParseFromString(compressed)
        return DtoMessage(uid=msg.uid, message=msg.message)
