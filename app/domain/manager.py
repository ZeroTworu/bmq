import asyncio
import signal
from signal import SIGABRT, SIGINT, SIGTERM, signal as signal_fn
from typing import TYPE_CHECKING

import aio_pika

from app.compress import get_compressor
from app.config.idle import IDLE_TIMEOUT
from app.config.rmq import RMQ_DSN
from app.config.types import AppMode
from app.domain.receiver import Receiver
from app.domain.replayer import Replayer
from app.im import get_bots
from app.domain.logger import censor_amqp, get_logger

if TYPE_CHECKING:
    from logging import Logger

    from aio_pika.robust_connection import AbstractRobustConnection

    from app.compress.icompress import ICompressor


class Manager:

    _rmq_conn: 'AbstractRobustConnection' = None
    _compressor: 'ICompressor' = None
    _logger: 'Logger' = None
    _mode: 'AppMode' = None
    _working: bool = False
    _amqp_wait_timeout: int = 5

    def __init__(self, mode: 'AppMode'):
        self._logger = get_logger('manage')
        self._logger.info('Starting...')

        self._mode = mode
        self._bots = get_bots()
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

    async def start(self):
        self._working = True
        await self._create_amqp_connection()

        match self._mode:
            case AppMode.RECEIVER:
                receiver = Receiver(self._rmq_conn, self._bots, self._compressor)
                await receiver.start()
            case AppMode.REPLAYER:
                replayer = Replayer(self._rmq_conn, self._bots, self._compressor)
                await replayer.start()

        await self._idle()

    async def _idle(self):
        while self._working:
            await asyncio.sleep(IDLE_TIMEOUT)

        await self._rmq_conn.close()

        for bot in self._bots.values():
            await bot.destroy()

        self._logger.info('Exit')

    async def _create_amqp_connection(self):
        try:
            self._rmq_conn = await aio_pika.connect_robust(RMQ_DSN)
            self._logger.info('RMQ connect to %s', censor_amqp(RMQ_DSN))
        except ConnectionError:
            self._logger.warning('Cannot connect to RMQ, wait %ss...', self._amqp_wait_timeout)
            await asyncio.sleep(self._amqp_wait_timeout)
            await self._create_amqp_connection()
