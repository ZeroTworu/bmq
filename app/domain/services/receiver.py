from typing import TYPE_CHECKING

from app.domain.services.iservice import IService

if TYPE_CHECKING:
    from app.im.dto import DtoMessage


class ReceiverService(IService):

    async def start(self):
        await super().start()

        self._logger.info('Starting receiver')

        for bot in self._bots.values():
            await bot.build()
            bot.register_message_callback(self._message_callback)

        self._logger.info('Service Receiver started')

    async def _message_callback(self, message: 'DtoMessage'):
        queue_name = f'bmq_{message.bot_type.value}'
        self._logger.info('Receive message from im "%s"', message)

        compressed = await self._compressor.compress(message)
        await self._message_bus.publish(queue_name, compressed)

        self._logger.info('Message %s published to %s', message, queue_name)
