from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from app.domain.logger import get_logger

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

    def __init__(
            self,
            rmq_conn: 'AbstractRobustConnection',
            bots: 'Dict[BotType, IBot]',
            compressor: 'ICompressor',
            name: str = 'service'
    ):
        self._logger = get_logger(name)
        self._bots = bots
        self._rmq_conn = rmq_conn
        self._compressor = compressor

    @abstractmethod
    async def start(self):
        pass
