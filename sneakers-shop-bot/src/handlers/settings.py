import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

import db
from src import messages
from src.modules.bot_helpers import delete_messages, remove_keyboard
from src.misc import dp
from src.messages.commands import callbacks_and_commands
from src.messages import commands
from src.states import SettingsStates
from src.modules import validation
from src.modules.bot_helpers import prepare_user_settings
import src.keyboards as kb
from src.handlers.general import start
from src.handlers.assortment_navigation import offer_shoes
from src.misc import bot


@dp.message_handler(commands='unreg')
async def unreg_cmd(message: types.Message):
    await db.unregister_user(message.from_user.id)
    await message.answer('Вы успешно удалили свой профиль')


@dp.message_handler(lambda message: message.text == commands.cancel, state=SettingsStates.nominal)
async def settings_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Изменение настроек отменено")

    await start(message)


@dp.message_handler(lambda message: message.text == commands.change_name, state=SettingsStates.phone_number)
async def settings_backto_name(message: types.Message):
    await settings_edition(message)


@dp.message_handler(lambda message: message.text == commands.change_phone, state=SettingsStates.contact_method)
async def settings_backto_phone(message: types.Message):
    await SettingsStates.phone_number.set()
    await message.answer(messages.phone_change,
                         reply_markup=kb.change_name)


@dp.message_handler(lambda x: x.text == callbacks_and_commands['settings'])
async def change_settings(message: types.Message):
    user_settings = await db.get_important_user_settings(message.from_user.id)
    if user_settings:
        user_settings = tuple(*user_settings)
        await message.answer(prepare_user_settings(*user_settings), reply_markup=kb.register_ikb)
    else:
        await settings_edition(message)


@dp.callback_query_handler(lambda c: c.data == 'change_settings')
async def change_settings_cb(callback: types.CallbackQuery):
    await remove_keyboard(callback.message)
    await change_settings(callback.message)


@dp.message_handler(commands='change_settings')
async def settings_edition(message: types.Message):
    await SettingsStates.nominal.set()
    await message.answer(messages.nominal,
                         reply_markup=kb.cancel)


@dp.message_handler(state=SettingsStates.nominal)
async def settings_nominal(message: types.Message, state: FSMContext, is_change: bool = False):
    if not is_change:
        nominal = message.text
        async with state.proxy() as data:
            data['nominal'] = nominal
        await message.answer(messages.phone(nominal))

    await SettingsStates.phone_number.set()
    await message.answer(messages.phone_change, reply_markup=kb.change_name)


@dp.message_handler(state=SettingsStates.phone_number)
async def settings_phone(message: types.Message, state: FSMContext):
    phone = message.text
    if validation.is_valid_phone(phone):
        async with state.proxy() as data:
            data['phone'] = phone
        await SettingsStates.contact_method.set()
        await message.answer(messages.contact_method_first, reply_markup=kb.change_phone)
        await message.answer(messages.contact_method_second, reply_markup=kb.payment_method)
    else:
        await message.answer('Введённый вами номер телефона не является корректным')
        await message.answer('Пожалуйста введите ваш номер телефона в формате +7(xxx)xxx-xx-xx')


contact_method_regexp = r'settings_contact_([^_]*)'


@dp.message_handler(lambda message: message.text == commands.change_phone, state=SettingsStates.contact_method)
async def settings_goback_contact(message: types.Message, state: FSMContext):
    await settings_nominal(message, state, is_change=True)


@dp.callback_query_handler(regexp=contact_method_regexp, state=SettingsStates.contact_method)
async def contact_method_cb(callback: types.CallbackQuery, state: FSMContext):
    method = callback.data.split('_')[-1]
    asyncio.create_task(remove_keyboard(callback.message))
    asyncio.create_task(callback.answer())
    async with state.proxy() as data:
        data['contact_method'] = method

    await SettingsStates.address.set()
    await callback.message.answer(messages.address, reply_markup=kb.change_contact_method)


@dp.message_handler(lambda message: message.text == commands.change_contact_method, state=SettingsStates.address)
async def settings_goback_address(message: types.Message, state: FSMContext):
    await SettingsStates.contact_method.set()
    await message.answer('Изменение метода связи 📞', reply_markup=kb.change_phone)
    await message.answer(messages.contact_method_second, reply_markup=kb.payment_method)


@dp.message_handler(state=SettingsStates.address)
async def settings_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

    await SettingsStates.payment_method.set()
    await message.answer(messages.payment_method_first, reply_markup=kb.change_address)
    await message.answer(messages.payment_method_second, reply_markup=kb.payment_types)


@dp.message_handler(lambda message: message.text == commands.change_address, state=SettingsStates.payment_method)
async def settings_goback_payment(message: types.Message, state: FSMContext):
    await SettingsStates.address.set()
    await message.answer(messages.address_change, reply_markup=kb.change_contact_method)


@dp.callback_query_handler(lambda c: c.data.startswith('payment_'), state=SettingsStates.payment_method)
async def settings_payment(callback: types.CallbackQuery, state: FSMContext):
    payment_method = callback.data.split('_')[1]

    async with state.proxy() as data:
        data['payment_method'] = payment_method
        phone = data['phone']
        nominal = data['nominal']
        address = data['address']
        contact_method = data['contact_method']

    asyncio.create_task(callback.message.delete())
    asyncio.create_task(callback.answer())
    await SettingsStates.confirm.set()
    await callback.message.answer(prepare_user_settings(nominal, phone, contact_method, address, payment_method),
                                  reply_markup=kb.confirm_settings)


@dp.message_handler(lambda message: message.text == commands.change_payment_method, state=SettingsStates.confirm)
async def settings_confirm_goback(message: types.Message):
    await SettingsStates.payment_method.set()
    await message.answer('Изменение метода оплаты 💰', reply_markup=kb.change_address)
    await message.answer(messages.payment_method_second, reply_markup=kb.payment_types)


@dp.callback_query_handler(lambda c: c.data == 'confirm_settings', state=SettingsStates.confirm)
async def confirm_settings(callback: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(remove_keyboard(callback.message))

    async with state.proxy() as data:
        payment_method = data['payment_method']
        phone = data['phone']
        nominal = data['nominal']
        address = data['address']
        contact_method = data['contact_method']

    user_id = callback.from_user.id
    user_link = callback.from_user.url
    await callback.message.answer("Ваши данные успешно сохранены, приятного пользования", reply_markup=kb.menu)
    if await db.get_user_settings(user_id):
        await db.update_user_settings(user_id, nominal, phone, address, payment_method, contact_method)
    else:
        await db.add_user_settings(user_id, user_link, nominal, phone, address, payment_method, contact_method)

    async with state.proxy() as data:
        if 'model' in data and 'brand' in data:
            brand, model = data['brand'],  data['model']
            await offer_shoes(callback.message, brand, model)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'apply_registration')
async def settings_edition_cb(callback: types.CallbackQuery):
    asyncio.create_task(callback.answer())
    await settings_edition(callback.message)
    await delete_messages(callback.from_user.id, callback.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'restart_registration', state=[SettingsStates.confirm, None])
async def settings_restart_cb(callback: types.CallbackQuery):
    asyncio.create_task(callback.answer())
    asyncio.create_task(remove_keyboard(callback.message))
    await settings_edition(callback.message)


@dp.callback_query_handler(lambda c: c.data == 'cancel_registration', state=SettingsStates.confirm)
async def settings_restart_cb(callback: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(callback.answer())
    asyncio.create_task(remove_keyboard(callback.message))
    await callback.message.answer("Регистрация отменена, возвращение в главное меню", reply_markup=kb.menu)
    await state.finish()


@dp.message_handler(state=SettingsStates)
async def delete_redundant_message(message: types.Message):
    await message.delete()
