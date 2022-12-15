from typing import TYPE_CHECKING

from app.config.app import BOT_TYPE_USED
from app.im.jabber.jabber_bot import JabberBot

from .._types import BotType
from .tg.tg_bot import TelegramBot

if TYPE_CHECKING:
    from typing import Dict, List

    from .ibot import IBot


def get_bots() -> 'Dict[BotType,IBot]':
    result: 'Dict[BotType,IBot]' = {}
    types: 'List[str]' = BOT_TYPE_USED.split(',')

    for _type in types:
        match BotType(_type):
            case BotType.JABBER:
                result[BotType.JABBER] = JabberBot()
            case BotType.TELEGRAM:
                result[BotType.TELEGRAM] = TelegramBot()

    return result
