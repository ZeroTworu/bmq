from typing import TYPE_CHECKING

from pyrogram import Client
from pyrogram.handlers import MessageHandler

from app.config.tg import TG_API_HASH, TG_API_ID, TG_BOT_TOKEN
from app.im.ibot import DtoMessage, IBot
from app.im.tg.filters import filter_not_bot
from app.logger import get_logger

if TYPE_CHECKING:
    from logging import Logger

    from pyrogram.types import Message

    from app.im.ibot import Callback


class TgMqBot(IBot, Client):

    _callback: 'Callback' = None
    _logger: 'Logger' = None

    def __init__(self):

        self._logger = get_logger('tg-core')

        super().__init__(
            name='MqBot',
            api_id=TG_API_ID,
            api_hash=TG_API_HASH,
            in_memory=True,
            bot_token=TG_BOT_TOKEN,
        )

    def register_message_callback(self, cb: 'Callback'):
        self._callback = cb
        self.add_handler(MessageHandler(self._pre_receive, filters=filter_not_bot))
        self._logger.debug('Registered callback %s', cb)

    async def _pre_receive(self, _, message: 'Message'):
        self._logger.debug(
            'Receive message "%s" from "%s" (%s)',
            message.text,
            message.from_user.id,
            message.from_user.username,
        )

        dto_message = DtoMessage(uid=str(message.from_user.id), message=message.text)
        await self._callback(dto_message)

    async def reply(self, message: 'DtoMessage'):
        self._logger.debug('Reply to "%s" with text "%s"', message.uid, message.message)
        await self.send_message(int(message.uid), message.message)

    async def init(self):
        await self.start()
        self._logger.info('Login as: "%s"', self.me.username)

    async def destroy(self):
        await self.stop()
