import asyncio

from aiogram.dispatcher import FSMContext

import db
from src.misc import dp, bot
from aiogram import types
import logging
from .. import messages
from ..modules.bot_helpers import update_text, notify_admins
from src.states import RefundStates

from .. import keyboards as kb


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await db.add_user(message.from_user.id, False)
    await message.answer(messages.greeting, reply_markup=kb.menu)


@dp.message_handler(commands='cancel', state='*')
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Отмена действия')


@dp.message_handler(commands='faq')
async def faq_cmd(message: types.Message):
    await message.answer(messages.faq)


@dp.message_handler(commands='refund')
async def refund_cmd(message: types.Message):
    await RefundStates.refund.set()
    await message.answer(messages.refund)


@dp.message_handler(state=RefundStates.refund)
async def refund_cmd(message: types.Message, state: FSMContext):
    asyncio.create_task(state.finish())
    detail = message.text

    user_settings = await db.get_user_settings(message.from_user.id)
    txt = f'''
<b>Получена новая заявка на возврат</b>
Комментарий пользователя: 
{detail}


<b>Покупатель</b>
<em>Имя: {user_settings['nominal']}</em>
<em>Ссылка на пользователя: {user_settings['username']}</em>
<em>Номер телефона: {user_settings['phone']}</em>
<em>Адрес: {user_settings['address']}</em>
<em>Метод оплаты: {user_settings['payment_method']}</em>
<em>Связаться: {user_settings['contact_method']}</em>    
    '''
    await notify_admins(txt)


@dp.callback_query_handler(text_startswith="delete_message_", state='*')
async def delete_message(callback: types.CallbackQuery):
    to_remove = int(callback.data.split('_')[-1])
    for i in range(to_remove):
        await bot.delete_message(callback.from_user.id, callback.message.message_id - i)
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data == "remove_keyboard", state='*')
async def remove_keyboard(callback: types.CallbackQuery):
    await update_text(callback.message, callback.message.text, keyboard=None)
    await callback.answer()
