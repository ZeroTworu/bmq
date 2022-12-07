from typing import TYPE_CHECKING

from app.config.types import BOT_TYPE, BotType

from .tg.tg_bot import TgMqBot

if TYPE_CHECKING:
    from .ibot import IBot


def get_bot() -> 'IBot':
    match BOT_TYPE:
        case BotType.TELEGRAM:
            return TgMqBot()
        case _:
            raise ValueError('Just now only Telegram supported')
