from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrogram.types import Message


def filter_not_bot(_, m: 'Message'):
    return not m.from_user.is_bot
