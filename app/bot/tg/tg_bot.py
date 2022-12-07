from pyrogram import Client
from pyrogram.handlers import MessageHandler
from app.bot.ibot import IBot, DtoMessage
from app.config.tg import TG_BOT_TOKEN, TG_API_HASH, TG_API_ID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrogram.types import Message
    from app.bot.ibot import Callback


class TgMqBot(IBot, Client):

    _callback: 'Callback' = None

    def __init__(self):

        super().__init__(
            name='MqBot',
            api_id=TG_API_ID,
            api_hash=TG_API_HASH,
            in_memory=True,
            bot_token=TG_BOT_TOKEN,
        )

    def register_message_callback(self, cb: 'Callback'):
        self._callback = cb
        self.add_handler(MessageHandler(self._pre_receive))

    async def _pre_receive(self, _, message: 'Message'):
        dto_message = DtoMessage(uid=message.from_user.id, message=message.text)
        await self._callback(dto_message)

    async def reply(self, message: 'DtoMessage'):
        await self.send_message(message.uid, message.message)

    async def init(self):
        await self.start()
