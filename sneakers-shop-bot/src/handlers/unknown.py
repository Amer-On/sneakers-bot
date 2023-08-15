import asyncio

from aiogram import types

from src.misc import dp
from src.modules.bot_helpers import unknown_message_reply
from src.modules.bot_helpers import remove_keyboard


@dp.message_handler()
async def unknown(message: types.Message):
    await unknown_message_reply(message)


@dp.callback_query_handler(lambda x: True, state='*')
async def unknown_cb(callback: types.CallbackQuery):
    asyncio.create_task(callback.answer('Действие недоступно'))
    asyncio.create_task(remove_keyboard(callback.message))
