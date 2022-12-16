import signal
from asyncio import sleep as async_sleep
from signal import SIGABRT, SIGINT, SIGTERM, signal as signal_fn
from typing import TYPE_CHECKING

from app._types import AppType
from app.config.app import IDLE_TIMEOUT
from app.domain.services import ReceiverService, ReplayerService
from app.logger import get_logger

if TYPE_CHECKING:
    from logging import Logger

    from app.domain.services import IService


class Manager:

    _logger: 'Logger' = None
    _mode: 'AppType' = None
    _working: bool = False
    _service: 'IService' = None

    def __init__(self, mode: 'AppType'):
        self._logger = get_logger('manage')
        self._logger.info('Starting...')

        self._mode = mode

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

        match self._mode:
            case AppType.RECEIVER:
                self._service = ReceiverService('receiver')
            case AppType.REPLAYER:
                self._service = ReplayerService('replayer')
            case _:
                raise ValueError(f'Unknown service {self._mode}')

        await self._service.start()
        await self._idle()

    async def _idle(self):
        while self._working:
            await async_sleep(IDLE_TIMEOUT)

        await self._service.stop()
        self._logger.info('Exit')
