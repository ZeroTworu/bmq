from abc import ABCMeta
from typing import TYPE_CHECKING

from app.bus import get_bus
from app.compress import get_compressor
from app.im import get_bots
from app.logger import get_logger

if TYPE_CHECKING:
    from logging import Logger
    from typing import TYPE_CHECKING, Dict

    from app._types import BotType
    from app.bus import IBus
    from app.compress import ICompressor
    from app.im import IBot


class IService(metaclass=ABCMeta):

    _bots: 'Dict[BotType, IBot]' = {}
    _logger: 'Logger' = None
    _name: str = None
    _message_bus: 'IBus' = None
    _compressor: 'ICompressor' = None

    def __init__(
            self,
            name: str = 'service'
    ):
        self._name = name
        self._logger = get_logger(name)
        self._bots = get_bots()
        self._compressor = get_compressor()
        self._message_bus = get_bus()

        self._logger.info(
            'Init %s with Bots: %s, Compressor: %s, Message Bus: %s',
            self._name,
            list(map(lambda bot: bot.name, self._bots)),
            self._compressor.name,
            self._message_bus.name,
        )

    async def start(self):
        await self._message_bus.connect()

    async def stop(self):
        await self._message_bus.close()

        for bot in self._bots.values():
            await bot.destroy()

        self._logger.info('Service %s stopped', self._name)
