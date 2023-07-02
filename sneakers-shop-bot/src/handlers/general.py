from aiogram.dispatcher import FSMContext

from src.misc import dp, bot
from aiogram import types
import logging
from .. import messages
from ..modules.bot_helpers import update_text, unknown_message_reply

from .. import keyboards as kb


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(messages.greeting, reply_markup=kb.menu)


@dp.message_handler(commands='cancel', state='*')
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Отмена действия')


@dp.message_handler()
async def general(message: types.Message):
    await unknown_message_reply(message)


@dp.callback_query_handler(text_startswith="delete_message_", state='*')
async def delete_message(callback: types.CallbackQuery):
    to_remove = int(callback.data.split('_')[-1])
    for i in range(to_remove):
        await bot.delete_message(callback.from_user.id, callback.message.message_id - i - 1)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data == "remove_keyboard", state='*')
async def remove_keyboard(callback: types.CallbackQuery):
    await update_text(callback.message, callback.message.text, keyboard=None)
    await callback.answer()
