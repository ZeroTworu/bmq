from asyncio import sleep as async_sleep
from typing import TYPE_CHECKING

from aio_pika import Message, connect_robust

from app.bus.ibus import IBus
from app.config.bus import RMQ_DSN
from app.logger import censor_amqp

if TYPE_CHECKING:
    from aio_pika.robust_connection import (
        AbstractIncomingMessage, AbstractRobustChannel,
        AbstractRobustConnection,
    )

    from app._types import BusCallback


class RabbitMqBus(IBus):

    _amqp_wait_timeout: int = 5
    _rmq_conn: 'AbstractRobustConnection' = None

    _channel: 'AbstractRobustChannel' = None

    _name: str = 'RabbitMQ Message Bus'

    def __init__(self):
        super().__init__('rmq-bus')

    async def connect(self):
        try:
            self._rmq_conn = await connect_robust(RMQ_DSN)
            self._channel = await self._rmq_conn.channel()
            await self._channel.set_qos(prefetch_count=100)
            self._logger.info('RMQ connect to %s', censor_amqp(RMQ_DSN))
        except ConnectionError:
            self._logger.warning('Cannot connect to RMQ, wait %ss...', self._amqp_wait_timeout)
            await async_sleep(self._amqp_wait_timeout)
            await self.connect()

    async def close(self):
        await self._channel.close()
        await self._rmq_conn.close()

    async def register_callback(self, queue_name: str, callback: 'BusCallback'):
        await super().register_callback(queue_name, callback)

        queue = await self._channel.declare_queue(queue_name, auto_delete=True)
        await queue.consume(self._process_message)

    async def _process_message(self, message: 'AbstractIncomingMessage'):
        self._logger.debug('Receive message from RMQ %s', message)

        if (callback := self._callbacks.get(message.routing_key)) is None:
            self._logger.warning('No callback for routing_key %s', message.routing_key)
            return

        await callback(message.body)
        await message.ack()

    async def publish(self, queue: str, message: bytes):
        self._logger.debug('RMQ publish message %s to %s', message, queue)

        await self._channel.default_exchange.publish(
            Message(body=message),
            routing_key=queue,
        )
