import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

import db
from src.misc import dp
from src.messages.commands import callbacks_and_commands
from src.states import SettingsStates
from src.modules import validation
import src.keyboards as kb


@dp.message_handler(lambda x: x.text == callbacks_and_commands['settings'])
async def settings_edition(message: types.Message):
    asyncio.create_task(SettingsStates.nominal.set())
    await message.answer("Пожалуйста представьтесь")


@dp.message_handler(state=SettingsStates.nominal)
async def settings_nominal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nominal'] = message.text

    asyncio.create_task(SettingsStates.phone_number.set())
    await message.answer("Теперь введите ваш номер телефона")


@dp.message_handler(state=SettingsStates.phone_number)
async def settings_phone(message: types.Message, state: FSMContext):
    phone = message.text
    if validation.is_valid_phone(phone):
        async with state.proxy() as data:
            data['phone'] = phone
        asyncio.create_task(SettingsStates.address.set())
        await message.answer("Номер телефона успешно сохранён")
        await message.answer("Введите адрес, на который будет произведена доставка")
    else:
        await message.answer('Введённый вами номер телефона не является корректным')
        await message.answer('Пожалуйста введите ваш номер телефона в формате +7(xxx)xxx-xx-xx')


@dp.message_handler(state=SettingsStates.address)
async def settings_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

    kb_ = kb.payment_types

    asyncio.create_task(SettingsStates.payment_method.set())
    await message.answer("Адрес успешно сохранён")
    await message.answer("Выберите метод оплаты", reply_markup=kb_)


@dp.callback_query_handler(lambda c: c.data.startswith('payment_'), state=SettingsStates.payment_method)
async def settings_payment(callback: types.CallbackQuery, state: FSMContext):
    payment_method = callback.data.split('_')[1]

    async with state.proxy() as data:
        phone = data['phone']
        nominal = data['nominal']
        address = data['address']

    user_id = callback.from_user.id
    user_link = callback.from_user.url
    asyncio.create_task(state.finish())
    asyncio.create_task(callback.message.delete())
    asyncio.create_task(callback.answer())
    await callback.message.answer("Ваши данные успешно сохранены, приятного пользования")
    if await db.get_user_settings(user_id):
        await db.update_user_settings(user_id, nominal, phone, address, payment_method)
    else:
        await db.add_user_settings(user_id, user_link, nominal, phone, address, payment_method)
