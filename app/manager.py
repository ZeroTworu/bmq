import asyncio
import signal
from signal import SIGABRT, SIGINT, SIGTERM, signal as signal_fn
from typing import TYPE_CHECKING

import aio_pika

from app.bot import get_bot
from app.compress import get_compressor
from app.config.idle import IDLE_TIMEOUT
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
    _mode: 'AppMode' = None
    _working: bool = False
    _amqp_wait_timeout: int = 5

    def __init__(self, mode: 'AppMode'):
        self._logger = get_logger('manage')
        self._mode = mode

        self._logger.info('init app in mode %s', mode)

        self._bot = get_bot()
        self._compressor = get_compressor()

        for s in (SIGINT, SIGTERM, SIGABRT):
            signal_fn(s, self.stop)

    def stop(self, signum, __):
        signal_name = {
            k: v for v, k in signal.__dict__.items()
            if v.startswith("SIG") and not v.startswith("SIG_")
        }[signum]

        self._logger.info('Stop signal received (%s). Exiting...', signal_name)
        self._working = False

    async def run(self):
        await self._create_amqp_connection()
        self._working = True

        match self._mode:
            case AppMode.RECEIVER:
                await self.receiver()
            case AppMode.REPLAYER:
                await self.replayer()

    async def receiver(self):
        self._logger.info('Starting receiver')

        await self._bot.init()
        self._bot.register_message_callback(self._message_callback)
        self._logger.info('Receiver started')

        await self._idle()

    async def _message_callback(self, message: 'DtoMessage'):
        self._logger.info('Receive message from bot "%s"', message)
        compressed = await self._compressor.compress(message)

        channel = await self._rmq_conn.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=compressed),
            routing_key=RMQ_ROUTING_KEY,
        )
        self._logger.info('Message %s published', message)

    async def replayer(self):
        self._logger.info('Starting replayer')

        await self._bot.init()
        channel = await self._rmq_conn.channel()
        await channel.set_qos(prefetch_count=100)

        queue = await channel.declare_queue(RMQ_QUEUE, auto_delete=True)
        await queue.consume(self._process_message)

        self._logger.info('Replayer started')
        await self._idle()

    async def _process_message(self, message: 'AbstractMessage'):
        self._logger.debug('Receive message from RMQ %s', message)

        dto_message = await self._compressor.decompress(message.body)

        self._logger.info('Decoded message from RMQ %s', dto_message)

        await self._bot.reply(dto_message)

    async def _idle(self):
        while self._working:
            await asyncio.sleep(IDLE_TIMEOUT)

        await self._rmq_conn.close()
        await self._bot.destroy()

    async def _create_amqp_connection(self):
        try:
            self._rmq_conn = await aio_pika.connect_robust(RMQ_DSN)
            self._logger.info('RMQ connect to %s', censor_amqp(RMQ_DSN))
        except ConnectionError:
            self._logger.warning('Cannot connect to RMQ, wait %ss...', self._amqp_wait_timeout)
            await asyncio.sleep(self._amqp_wait_timeout)
            await self._create_amqp_connection()
