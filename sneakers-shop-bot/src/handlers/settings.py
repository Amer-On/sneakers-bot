import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

import db
from src import messages
from src.modules.bot_helpers import delete_messages, remove_keyboard
from src.misc import dp
from src.messages.commands import callbacks_and_commands
from src.states import SettingsStates
from src.modules import validation
import src.keyboards as kb


@dp.message_handler(lambda x: x.text == callbacks_and_commands['settings'])
async def settings_edition(message: types.Message):
    asyncio.create_task(SettingsStates.nominal.set())
    await message.answer(messages.nominal, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=SettingsStates.nominal)
async def settings_nominal(message: types.Message, state: FSMContext):
    nominal = message.text
    async with state.proxy() as data:
        data['nominal'] = nominal

    asyncio.create_task(SettingsStates.phone_number.set())
    await message.answer(messages.phone(nominal))


@dp.message_handler(state=SettingsStates.phone_number)
async def settings_phone(message: types.Message, state: FSMContext):
    phone = message.text
    if validation.is_valid_phone(phone):
        async with state.proxy() as data:
            data['phone'] = phone
        asyncio.create_task(SettingsStates.contact_method.set())
        await message.answer("Номер телефона успешно сохранён")
        await message.answer(messages.contact_method, reply_markup=kb.payment_method)
    else:
        await message.answer('Введённый вами номер телефона не является корректным')
        await message.answer('Пожалуйста введите ваш номер телефона в формате +7(xxx)xxx-xx-xx')


contact_method_regexp = r'settings_contact_([^_]*)'


@dp.callback_query_handler(regexp=contact_method_regexp, state=SettingsStates.contact_method)
async def contact_method_cb(callback: types.CallbackQuery, state: FSMContext):
    method = callback.data.split('_')[-1]
    asyncio.create_task(remove_keyboard(callback.message))
    async with state.proxy() as data:
        data['contact_method'] = method

    asyncio.create_task(SettingsStates.address.set())
    await callback.message.answer(messages.address)


@dp.message_handler(state=SettingsStates.address)
async def settings_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

    kb_ = kb.payment_types

    asyncio.create_task(SettingsStates.payment_method.set())
    await message.answer(messages.payment_method, reply_markup=kb_)


@dp.callback_query_handler(lambda c: c.data.startswith('payment_'), state=SettingsStates.payment_method)
async def settings_payment(callback: types.CallbackQuery, state: FSMContext):
    payment_method = callback.data.split('_')[1]

    async with state.proxy() as data:
        phone = data['phone']
        nominal = data['nominal']
        address = data['address']
        contact_method = data['contact_method']

    user_id = callback.from_user.id
    user_link = callback.from_user.url
    asyncio.create_task(state.finish())
    asyncio.create_task(callback.message.delete())
    asyncio.create_task(callback.answer())
    await callback.message.answer("Ваши данные успешно сохранены, приятного пользования", reply_markup=kb.menu)
    if await db.get_user_settings(user_id):
        await db.update_user_settings(user_id, nominal, phone, address, payment_method, contact_method)
    else:
        await db.add_user_settings(user_id, user_link, nominal, phone, address, payment_method, contact_method)


@dp.callback_query_handler(lambda c: c.data == 'apply_registration')
async def settings_edition_cb(callback: types.CallbackQuery):
    asyncio.create_task(callback.answer())
    await settings_edition(callback.message)
    await delete_messages(callback.from_user.id, callback.message.message_id)

