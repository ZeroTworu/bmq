from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app._types import BotType


@dataclass
class DtoMessage:
    uid: str
    message: str
    bot_type: 'BotType|None' = None

    def __str__(self):
        return f'<(uid={self.uid}) (message={self.message}) (bot_type={self.bot_type})>'
