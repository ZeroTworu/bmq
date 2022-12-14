from typing import TYPE_CHECKING

from aioxmpp.service import Service, depsignal
from aioxmpp.stream import StanzaStream

if TYPE_CHECKING:
    from typing import Awaitable, Callable, Dict

    from aioxmpp import Message, MessageType

    PreReceiveCallback = Callable[[Message], Awaitable]


class AsyncMessageDispatcher(Service):
    _map: 'Dict[MessageType, PreReceiveCallback]' = {}

    @property
    def local_jid(self):
        return self.client.local_jid

    @depsignal(StanzaStream, "on_message_received", defer=True)
    async def _feed(self, stanza):

        try:
            await self._map[stanza.type_](stanza)
        except KeyError:
            pass

    def register_callback(self, type_: 'MessageType', cb: 'PreReceiveCallback'):

        if type_ in self._map:
            raise ValueError(
                "only one listener allowed per matcher"
            )

        self._map[type_] = cb
