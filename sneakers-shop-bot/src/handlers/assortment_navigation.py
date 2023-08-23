import asyncio
import collections

from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
import re

import db
from src.modules.bot_helpers import notify_admins
from src.states import AssortmentStates
from ..misc import dp
from ..messages.commands import callbacks_and_commands
from .. import keyboards as kb
from .. import messages
from ..modules.bot_helpers import update_text


@dp.message_handler(lambda x: x.text == callbacks_and_commands['assortment_search'])
async def assortment_search(message: types.Message, state: FSMContext):
    await AssortmentStates.search.set()
    await message.answer("Напишите название модели👟", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=AssortmentStates.search)
async def assortment_search_back(message: types.Message, state: FSMContext):
    data = await db.search_models(message.text.lower())
    if data:
        _kb = kb.create_search_ikb(data)
        await message.answer(messages.successful_search, reply_markup=kb.menu)
        await message.answer(messages.search_results, reply_markup=_kb)
    else:
        await message.answer(messages.failed_search, reply_markup=kb.menu)

    await state.reset_state(with_data=False)


@dp.message_handler(lambda x: x.text == callbacks_and_commands['assortment_navigation'])
async def assortment(message: types.Message):
    brands = await db.get_stock_brands()
    _kb = kb.create_brands_ikb(brands)
    await message.answer(messages.assortment, reply_markup=_kb)


brand_regex = "get_([^_]*)_assortment"


@dp.callback_query_handler(regexp=brand_regex)
async def company_assortment(callback: types.CallbackQuery):
    brand = re.search(brand_regex, callback.data).group(1)
    models = await db.get_stock_models(brand)
    _kb = kb.create_models_ikb(brand, models)
    await update_text(callback.message, f"{brand} MODELS", keyboard=_kb)
    await callback.answer()


model_regex = "get_([^_]*)_([^_]*)_assortment"


@dp.callback_query_handler(regexp=model_regex)
async def model_assortment(callback: types.CallbackQuery):
    asyncio.create_task(callback.answer())
    brand, model = re.search(model_regex, callback.data).groups()

    await model_stock(callback.message, brand, model)


async def model_stock(message: types.Message, brand: str, model: str):
    photos_task = asyncio.create_task(db.get_photos(brand, model))
    sizes_task = asyncio.create_task(db.get_stock_size(brand, model))
    price_task = asyncio.create_task(db.get_price(brand, model))

    photos, sizes, price = await asyncio.gather(photos_task, sizes_task, price_task)

    n = 1
    if photos:
        media = types.MediaGroup()
        for el in photos:
            media.attach_photo(photo=el)

        await message.answer_media_group(media)
        n += len(photos)

    kb_ = kb.create_order_ikb(brand, model, n)

    await message.answer(
        f"{brand} {model}\nДоступные размеры: {', '.join(map(str, sizes))}\n"
        f"Стоимость: <b>{str(price) + ' руб.' if price else 'Неизвестно'}</b>",
        reply_markup=kb_)


order_regex = "order_([^_]*)_([^_]*)_create"


@dp.callback_query_handler(regexp=order_regex)
async def order_choose_size(callback: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(callback.answer())

    brand, model = re.search(order_regex, callback.data).groups()
    if not await db.get_user_settings(callback.from_user.id):
        async with state.proxy() as data:
            data['brand'] = brand
            data['model'] = model

        await callback.message.answer(messages.ask_to_register, reply_markup=kb.apply_registration)
        return

    await offer_shoes(callback.message, brand, model)


async def offer_shoes(message: types.Message, brand: str, model: str):
    sizes = await db.get_stock_size(brand, model)

    msg_txt = f"""
    Выберите размер кроссовок {brand} {model}
    """
    kb_ = kb.create_sizes_ikb(sizes, brand, model)

    await message.answer(msg_txt, reply_markup=kb_)


sizes_regex = 'order_([^_]*)_([^_]*)_([^_]*)_assortment'


@dp.callback_query_handler(regexp=sizes_regex)
async def order_model(callback: types.CallbackQuery):
    asyncio.create_task(callback.message.delete())
    asyncio.create_task(callback.answer())

    brand, model, size = re.search(sizes_regex, callback.data).groups()
    price = await db.get_price(brand, model)

    order_id = await db.create_order(callback.from_user.id, brand, model, size)
    msg_txt = f"""<b>Заказ №{order_id} успешно создан!</b>\n\n<b>Детали заказа:</b>
<em>Бренд:</em> {brand}
<em>Модель:</em> {model}
<em>Размер:</em> {size}
<em>Стоимость:</em> <b>{str(price) + " руб." if price else "Неизвестно"}</b>
    """
    await callback.message.answer(msg_txt)

    user_settings = await db.get_user_settings(callback.from_user.id)
    admins_message_text = f"""<b>Получен новый Заказ №{order_id}!</b>\n\n<b>Детали заказа:</b>
<em>Бренд:</em> {brand}
<em>Модель:</em> {model}
<em>Размер:</em> {size}
<em>Стоимость:</em> <b>{price} руб.</b>
    
<b>Покупатель</b>
<em>Имя: {user_settings['nominal']}</em>
<em>Ссылка на пользователя: {user_settings['username']}</em>
<em>Номер телефона: {user_settings['phone']}</em>
<em>Адрес: {user_settings['address']}</em>
<em>Метод оплаты: {user_settings['payment_method']}</em>
<em>Связаться: {user_settings['contact_method']}</em>
"""

    asyncio.create_task(notify_admins(admins_message_text))
