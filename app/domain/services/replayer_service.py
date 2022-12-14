from typing import TYPE_CHECKING

from app.config.types import BotType
from app.domain.services.iservice import IService

if TYPE_CHECKING:
    from aio_pika.message import AbstractIncomingMessage


class ReplayerService(IService):

    async def start(self):
        await super().start()

        channel = await self._rmq_conn.channel()
        await channel.set_qos(prefetch_count=100)

        for bot in self._bots.values():
            await bot.build()
            queue = await channel.declare_queue(f'bmq_{bot.str_type}', auto_delete=True)
            await queue.consume(self._process_message)

        self._logger.info('Service Replayer started')

    async def _process_message(self, message: 'AbstractIncomingMessage'):
        self._logger.debug('Receive message from RMQ %s', message)

        bot_type_str = message.routing_key.replace('bmq_', '')
        dto_message = await self._compressor.decompress(message.body)
        dto_message.bot_type = BotType(bot_type_str)

        self._logger.info('Decoded message from RMQ %s', dto_message)

        bot = self._bots.get(dto_message.bot_type)
        if bot is None:
            self._logger.error('Bot "%s" not registered', bot_type_str)
            return

        await bot.reply(dto_message)
        await message.ack()
