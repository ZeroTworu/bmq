from abc import ABCMeta
from asyncio import sleep as async_sleep
from typing import TYPE_CHECKING

import aio_pika

from app.compress import get_compressor
from app.config.rmq import RMQ_DSN
from app.domain.logger import censor_amqp, get_logger
from app.im import get_bots

if TYPE_CHECKING:
    from logging import Logger
    from typing import TYPE_CHECKING, Dict

    from aio_pika.robust_connection import AbstractRobustConnection

    from app.compress.icompress import ICompressor
    from app.config.types import BotType
    from app.im.ibot import IBot


class IService(metaclass=ABCMeta):

    _bots: 'Dict[BotType, IBot]' = {}
    _rmq_conn: 'AbstractRobustConnection' = None
    _logger: 'Logger' = None
    _name: str = None
    _rmq_conn: 'AbstractRobustConnection' = None
    _compressor: 'ICompressor' = None
    _amqp_wait_timeout: int = 5

    def __init__(
            self,
            name: str = 'service'
    ):
        self._name = name
        self._logger = get_logger(name)
        self._bots = get_bots()
        self._compressor = get_compressor()

    async def start(self):
        self._logger.info('Service %s starting...')
        await self._create_amqp_connection()

    async def stop(self):
        await self._rmq_conn.close()

        for bot in self._bots.values():
            await bot.destroy()

        self._logger.info('Service %s stopped', self._name)

    async def _create_amqp_connection(self):
        try:
            self._rmq_conn = await aio_pika.connect_robust(RMQ_DSN)
            self._logger.info('RMQ connect to %s', censor_amqp(RMQ_DSN))
        except ConnectionError:
            self._logger.warning('Cannot connect to RMQ, wait %ss...', self._amqp_wait_timeout)
            await async_sleep(self._amqp_wait_timeout)
            await self._create_amqp_connection()
