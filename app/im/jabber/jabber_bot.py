from typing import TYPE_CHECKING

from aioxmpp import (
    JID, Message, MessageType, PresenceManagedClient, PresenceShow,
    PresenceState, make_security_layer,
)

from app._types import BotType, DtoMessage
from app.config.jabber import JABBER_PASSWORD, JABBER_UID
from app.im.ibot import IBot
from app.im.jabber.dispatcher import AsyncMessageDispatcher
from app.logger import get_logger

if TYPE_CHECKING:
    from logging import Logger

    from app._types import MessageCallback


class JabberBot(PresenceManagedClient, IBot):
    _type: 'BotType' = BotType.JABBER

    def __init__(self):
        self._logger: 'Logger' = get_logger('jabber-core')
        self._callback: 'MessageCallback|None' = None

        super().__init__(JID.fromstr(JABBER_UID), make_security_layer(JABBER_PASSWORD))
        self._message_dispatcher: 'AsyncMessageDispatcher' = self.summon(AsyncMessageDispatcher)

    def register_message_callback(self, callback: 'MessageCallback'):
        self._callback = callback

        self._message_dispatcher.register_callback(
            MessageType.CHAT,
            self._pre_receive
        )

    async def _pre_receive(self, message: 'Message'):

        if message.type_ != MessageType.CHAT or bool(message.body.values()):
            return

        jid = f'{message.from_.localpart}@{message.from_.domain}'
        self._logger.debug('Received message from %s, message %s', jid, message)

        msg = DtoMessage(
            uid=jid,
            message=message.body[message.lang],
            bot_type=self._type,
        )

        await self._callback(msg)

    async def reply(self, message: 'DtoMessage'):
        msg = Message(
            to=JID.fromstr(message.uid),
            type_=MessageType.CHAT,
        )
        msg.body[None] = message.message
        await self.send(msg)

    async def build(self):
        self.start()
        self.set_presence(
            PresenceState(available=True, show=PresenceShow.CHAT),
            'Echo Bot',
        )
        self._logger.info('Jabber login as %s', JABBER_UID)

    async def destroy(self):
        self.stop()
        self._logger.info('Jabber bot destroyed')
