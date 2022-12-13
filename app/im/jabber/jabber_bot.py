from asyncio import get_running_loop
from typing import TYPE_CHECKING

from aioxmpp import (
    JID, Message, MessageType, PresenceManagedClient, PresenceShow,
    PresenceState, make_security_layer,
)

from app.config.jabber import JABBER_UID, JABBER_PASSWORD
from app.config.types import BotType
from app.domain.logger import get_logger
from app.im.ibot import DtoMessage, IBot

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from logging import Logger

    from app.im.ibot import Callback


class JabberBot(PresenceManagedClient, IBot):
    _callback: 'Callback' = None
    _logger: 'Logger' = None
    _loop: 'AbstractEventLoop' = None
    _type: 'BotType' = BotType.JABBER

    def __init__(self):
        self._logger = get_logger('jabber-core')

        super().__init__(JID.fromstr(JABBER_UID), make_security_layer(JABBER_PASSWORD))

    def register_message_callback(self, callback: 'Callback'):
        self._callback = callback
        self.stream.register_message_callback(
            None,
            None,
            self._pre_receive,
        )

    def _pre_receive(self, message: 'Message'):
        jid = f'{message.from_.localpart}@{message.from_.domain}'
        self._logger.debug('Received message from %s', jid)

        msg = DtoMessage(
            uid=jid,
            message=message.body[message.lang],
            bot_type=self._type,
        )

        self._loop.create_task(self._callback(msg))

    async def reply(self, message: 'DtoMessage'):
        msg = Message(
            to=JID.fromstr(message.uid),
            type_=MessageType.CHAT,
        )
        msg.body[None] = message.message
        await self.send(msg)

    async def build(self):
        self._loop = get_running_loop()
        self.start()
        self.set_presence(
            PresenceState(available=True, show=PresenceShow.CHAT),
            'Echo Bot',
        )
        self._logger.info('Jabber login as %s', JABBER_UID)

    async def destroy(self):
        self.stop()
        self._logger.info('Jabber bot destroyed')
