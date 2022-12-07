from app.bot import get_bot
from typing import TYPE_CHECKING
from app.config.types import AppMode
from app.config.rmq import RMQ_DSN, RMQ_QUEUE, RMQ_ROUTING_KEY
import asyncio
import aio_pika
from compressor import get_compressor


if TYPE_CHECKING:
    from app.bot.ibot import IBot, DtoMessage
    from aio_pika.robust_connection import AbstractRobustConnection
    from aio_pika.message import IncomingMessage
    from compressor import ICompressor


class Manager:

    _bot: 'IBot' = None
    _rmq_conn: 'AbstractRobustConnection' = None
    _compressor: 'ICompressor' = None

    def __init__(self):
        self._bot = get_bot()
        self._compressor = get_compressor()

    async def run(self, mode: 'AppMode'):
        self._rmq_conn = await aio_pika.connect_robust(RMQ_DSN)
        match mode:
            case AppMode.RECEIVER:
                await self.receiver()
            case AppMode.REPLAYER:
                await self.replayer()

    async def receiver(self):
        await self._bot.init()
        self._bot.register_message_callback(self._message_callback)
        while True:
            await asyncio.sleep(1)

    async def _message_callback(self, message: 'DtoMessage'):
        print(f'out -> {message}')
        compressed = await self._compressor.compress(message)

        async with self._rmq_conn:
            channel = await self._rmq_conn.channel()

            await channel.default_exchange.publish(
                aio_pika.Message(body=compressed),
                routing_key=RMQ_ROUTING_KEY,
            )

    async def replayer(self):
        await self._bot.init()
        channel = await self._rmq_conn.channel()
        await channel.set_qos(prefetch_count=100)

        queue = await channel.declare_queue(RMQ_QUEUE, auto_delete=True)

        await queue.consume(self._process_message)

        try:
            await asyncio.Future()
        finally:
            await self._rmq_conn.close()

    async def _process_message(self, message: 'IncomingMessage'):
        dto_message = await self._compressor.decompress(message.body)
        await self._bot.reply(dto_message)
