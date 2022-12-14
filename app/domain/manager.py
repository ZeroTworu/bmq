import asyncio
import signal
from signal import SIGABRT, SIGINT, SIGTERM, signal as signal_fn
from typing import TYPE_CHECKING

from app.compress import get_compressor
from app.config.idle import IDLE_TIMEOUT
from app.config.types import AppMode
from app.domain.logger import get_logger
from app.domain.services.receiver_service import ReceiverService
from app.domain.services.replayer_service import ReplayerService

if TYPE_CHECKING:
    from logging import Logger

    from app.domain.services.iservice import IService


class Manager:

    _logger: 'Logger' = None
    _mode: 'AppMode' = None
    _working: bool = False
    _service: 'IService' = None

    def __init__(self, mode: 'AppMode'):
        self._logger = get_logger('manage')
        self._logger.info('Starting...')

        self._mode = mode
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

        match self._mode:
            case AppMode.RECEIVER:
                self._service = ReceiverService('receiver')
            case AppMode.REPLAYER:
                self._service = ReplayerService('replayer')
            case _:
                raise ValueError(f'Unknown service {self._mode}')

        await self._service.start()
        await self._idle()

    async def _idle(self):
        while self._working:
            await asyncio.sleep(IDLE_TIMEOUT)

        await self._service.stop()
        self._logger.info('Exit')
