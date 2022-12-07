import asyncio
from typing import TYPE_CHECKING

import aio_pika

from app.bot import get_bot
from app.compress import get_compressor
from app.config.rmq import RMQ_DSN, RMQ_QUEUE, RMQ_ROUTING_KEY
from app.config.types import AppMode
from app.logger import censor_amqp, get_logger

if TYPE_CHECKING:
    from logging import Logger

    from aio_pika.message import AbstractMessage
    from aio_pika.robust_connection import AbstractRobustConnection

    from app.bot.ibot import DtoMessage, IBot
    from app.compress.icompress import ICompressor


class Manager:

    _bot: 'IBot' = None
    _rmq_conn: 'AbstractRobustConnection' = None
    _compressor: 'ICompressor' = None
    _logger: 'Logger' = None

    def __init__(self):
        self._logger = get_logger('manage')
        self._logger.info('init app')

        self._bot = get_bot()
        self._compressor = get_compressor()

    async def run(self, mode: 'AppMode'):
        self._rmq_conn = await aio_pika.connect_robust(RMQ_DSN)
        self._logger.info('RMQ connect to %s', censor_amqp(RMQ_DSN))

        match mode:
            case AppMode.RECEIVER:
                await self.receiver()
            case AppMode.REPLAYER:
                await self.replayer()

    async def receiver(self):
        self._logger.info('starting receiver')
        await self._bot.init()
        self._bot.register_message_callback(self._message_callback)
        self._logger.info('receiver started')
        while True:
            await asyncio.sleep(1)

    async def _message_callback(self, message: 'DtoMessage'):
        self._logger.info('receive message from bot "%s"', message)
        compressed = await self._compressor.compress(message)

        channel = await self._rmq_conn.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=compressed),
            routing_key=RMQ_ROUTING_KEY,
        )
        self._logger.info('message %s published', message)

    async def replayer(self):
        self._logger.info('starting replayer')

        await self._bot.init()
        channel = await self._rmq_conn.channel()
        await channel.set_qos(prefetch_count=100)

        queue = await channel.declare_queue(RMQ_QUEUE, auto_delete=True)
        await queue.consume(self._process_message)

        self._logger.info('replayer started')

        try:
            await asyncio.Future()
        finally:
            await self._rmq_conn.close()

    async def _process_message(self, message: 'AbstractMessage'):
        self._logger.debug('receive message from RMQ %s', message)

        dto_message = await self._compressor.decompress(message.body)

        self._logger.info('decoded message from RMQ %s', dto_message)

        await self._bot.reply(dto_message)
