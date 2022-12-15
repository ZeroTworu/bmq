from asyncio import ensure_future, sleep as async_sleep
from typing import TYPE_CHECKING

from aioredis import from_url

from app.bus.ibus import IBus
from app.config.bus import REDIS_DSN

if TYPE_CHECKING:
    from aioredis.client import PubSub, Redis

    from app._types import BusCallback


class RedisBus(IBus):

    _redis: 'Redis' = None
    _wait_timeout: float = 0.1
    _working: bool = False
    _name: str = 'Redis Message Bus'

    def __init__(self):
        super().__init__('redis-bus')

    async def connect(self):
        self._redis = await from_url(REDIS_DSN)
        self._working = True

    async def close(self):
        await self._redis.close()
        self._working = False

    async def register_callback(self, queue_name: str, callback: 'BusCallback'):
        await super().register_callback(queue_name, callback)
        pubsub = self._redis.pubsub()
        await pubsub.psubscribe(queue_name)
        ensure_future(self._pre_receive_message(pubsub))

    async def publish(self, queue: str, message: bytes):
        self._logger.debug('Redis publish message %s to %s', message, queue)
        await self._redis.publish(queue, message)

    async def _pre_receive_message(self, channel: 'PubSub'):
        while self._working:

            if (message := await channel.get_message(ignore_subscribe_messages=True)) is None:
                continue

            channel_name = message.get('channel', b'').decode()
            if (callback := self._callbacks.get(channel_name)) is None:
                self._logger.warning('No callback for channel %s', channel_name)
                continue

            await callback(message.get('data'))
            await async_sleep(self._wait_timeout)
