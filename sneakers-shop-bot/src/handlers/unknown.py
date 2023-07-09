from aiogram import types

from src.misc import dp
from src.modules.bot_helpers import unknown_message_reply


@dp.message_handler()
async def unknown(message: types.Message):
    await unknown_message_reply(message)
