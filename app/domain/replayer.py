from typing import TYPE_CHECKING

from app.config.types import BotType
from app.domain.logger import get_logger

if TYPE_CHECKING:
    from logging import Logger
    from typing import TYPE_CHECKING, Dict

    from aio_pika.message import AbstractIncomingMessage
    from aio_pika.robust_connection import AbstractRobustConnection

    from app.compress.icompress import ICompressor
    from app.im.ibot import IBot


class Replayer:

    _logger: 'Logger' = None
    _bots: 'Dict[BotType, IBot]' = {}
    _compressor: 'ICompressor' = None
    _rmq_conn: 'AbstractRobustConnection' = None

    def __init__(
            self,
            rmq_conn: 'AbstractRobustConnection',
            bots: 'Dict[BotType, IBot]',
            compressor: 'ICompressor',
    ):

        self._logger = get_logger('replayer')
        self._bots = bots
        self._rmq_conn = rmq_conn
        self._compressor = compressor

    async def start(self):
        self._logger.info('Starting replayer')

        for bot in self._bots.values():
            await bot.init()

        channel = await self._rmq_conn.channel()
        await channel.set_qos(prefetch_count=100)

        for bot in self._bots.values():
            queue = await channel.declare_queue(f'bmq_{bot.str_type}', auto_delete=True)
            await queue.consume(self._process_message)

        self._logger.info('Replayer started')

    async def _process_message(self, message: 'AbstractIncomingMessage'):
        self._logger.debug('Receive message from RMQ %s', message)

        dto_message = await self._compressor.decompress(message.body)
        dto_message.bot_type = BotType(message.routing_key)

        self._logger.info('Decoded message from RMQ %s', dto_message)

        bot = self._bots.get(BotType(message.routing_key.replace('bmq_', '')))
        if bot is None:
            self._logger.error('Bot "%s" not registered', message.routing_key)
            return

        await bot.reply(dto_message)
        await message.ack()
