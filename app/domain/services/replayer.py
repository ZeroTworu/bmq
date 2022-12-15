from functools import partial

from app._types import BotType
from app.domain.services.iservice import IService


class ReplayerService(IService):

    async def start(self):
        await super().start()

        for bot in self._bots.values():
            await bot.build()

            callback = partial(self._process_message, bot_str_type=bot.str_type)
            queue_name = f'bmq_{bot.str_type}'
            self._logger.debug('Registered callback %s, on queue %s', callback, queue_name)

            await self._message_bus.register_callback(queue_name, callback)

        self._logger.info('Service Replayer started')

    async def _process_message(self, message: bytes, bot_str_type: str):
        self._logger.debug('Receive message from RMQ %s', message)

        dto_message = await self._compressor.decompress(message)
        dto_message.bot_type = BotType(bot_str_type)

        self._logger.info('Decoded message from %s %s', self._message_bus.name, dto_message)

        bot = self._bots.get(dto_message.bot_type)
        if bot is None:
            self._logger.error('Bot "%s" not registered', bot_str_type)
            return

        await bot.reply(dto_message)
