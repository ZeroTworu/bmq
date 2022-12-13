from typing import TYPE_CHECKING

from aio_pika import Message

from app.config.types import BotType
from app.domain.logger import get_logger

if TYPE_CHECKING:
    from logging import Logger
    from typing import TYPE_CHECKING, Dict

    from aio_pika.robust_connection import AbstractRobustConnection

    from app.compress.icompress import ICompressor
    from app.im.ibot import DtoMessage, IBot


class Receiver:
    _bots: 'Dict[BotType, IBot]' = {}
    _rmq_conn: 'AbstractRobustConnection' = None
    _logger: 'Logger' = None

    def __init__(
            self,
            rmq_conn: 'AbstractRobustConnection',
            bots: 'Dict[BotType, IBot]',
            compressor: 'ICompressor',
    ):
        self._logger = get_logger('receiver')
        self._bots = bots
        self._rmq_conn = rmq_conn
        self._compressor = compressor

    async def start(self):
        self._logger.info('Starting receiver')

        for bot in self._bots.values():
            await bot.init()
            bot.register_message_callback(self._message_callback)

        self._logger.info('Receiver started')

    async def _message_callback(self, message: 'DtoMessage'):
        self._logger.info('Receive message from im "%s"', message)
        compressed = await self._compressor.compress(message)

        channel = await self._rmq_conn.channel()

        await channel.default_exchange.publish(
            Message(body=compressed),
            routing_key=f'bmq_{message.bot_type.value}',
        )

        self._logger.info('Message %s published', message)
