from typing import TYPE_CHECKING

from aio_pika import Message

from app.domain.services.iservice import IService

if TYPE_CHECKING:
    from app.im.ibot import DtoMessage


class ReceiverService(IService):

    async def start(self):
        await super().start()

        self._logger.info('Starting receiver')

        for bot in self._bots.values():
            await bot.build()
            bot.register_message_callback(self._message_callback)

        self._logger.info('Service Receiver started')

    async def _message_callback(self, message: 'DtoMessage'):
        self._logger.info('Receive message from im "%s"', message)
        compressed = await self._compressor.compress(message)

        channel = await self._rmq_conn.channel()

        await channel.default_exchange.publish(
            Message(body=compressed),
            routing_key=f'bmq_{message.bot_type.value}',
        )

        self._logger.info('Message %s published', message)
