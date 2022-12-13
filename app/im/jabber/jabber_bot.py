from asyncio import get_running_loop
from typing import TYPE_CHECKING

from aioxmpp import (
    JID, Message, MessageType, PresenceManagedClient, PresenceShow,
    PresenceState, make_security_layer,
)

from app.config.jabber import JABBER_ID, JABBER_PASSWORD
from app.im.ibot import DtoMessage, IBot
from app.logger import get_logger

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from logging import Logger

    from app.im.ibot import Callback


class JabberBot(PresenceManagedClient, IBot):
    _callback: 'Callback' = None
    _logger: 'Logger' = None
    _loop: 'AbstractEventLoop' = None

    def __init__(self):
        self._logger = get_logger('jabber-core')

        super().__init__(JID.fromstr(JABBER_ID), make_security_layer(JABBER_PASSWORD), logger=self._logger)

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
        )

        self._loop.create_task(self._callback(msg))

    async def reply(self, message: 'DtoMessage'):
        msg = Message(
            to=JID.fromstr(message.uid),
            type_=MessageType.CHAT,
        )
        msg.body[None] = message.message
        await self.send(msg)

    async def init(self):
        self._loop = get_running_loop()
        self.start()
        self.set_presence(
            PresenceState(available=True, show=PresenceShow.CHAT),
            'Echo Bot',
        )
        self._logger.info('Login as %s', JABBER_ID)

    async def destroy(self):
        self.stop()
