import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
import re

import db
from ..misc import dp
from ..messages.commands import callbacks_and_commands
from .. import keyboards as kb
from .. import messages
from ..modules.bot_helpers import update_text


@dp.message_handler(lambda x: x.text == callbacks_and_commands['assortment_navigation'])
async def assortment(message: types.Message, state: FSMContext):
    brands = await db.get_brands()
    _kb = kb.create_brands_ikb(brands)
    await message.answer(messages.assortment, reply_markup=_kb)


brand_regex = "get_([^_]*)_assortment"


@dp.callback_query_handler(regexp=brand_regex)
async def company_assortment(callback: types.CallbackQuery):
    brand = re.search(brand_regex, callback.data).group(1)
    models = tuple(el[1] for el in await db.get_models(brand))
    _kb = kb.create_models_ikb(brand, models)
    await update_text(callback.message, f"{brand} MODELS", keyboard=_kb)
    await callback.answer()


model_regex = "get_([^_]*)_([^_]*)_assortment"


@dp.callback_query_handler(regexp=model_regex)
async def model_assortment(callback: types.CallbackQuery):
    brand, model = re.search(model_regex, callback.data).groups()

    photos_task = asyncio.create_task(db.get_photos(brand, model))
    sizes_task = asyncio.create_task(db.get_stock_size(brand, model))

    photos, sizes = await asyncio.gather(photos_task, sizes_task)

    media = types.MediaGroup()
    for el in photos:
        media.attach_photo(photo=el)

    kb_ = kb.create_order_ikb(brand, model, len(photos))

    await callback.message.answer_media_group(media)
    await callback.message.answer(f"{brand} {model}\nAvailable sizes: {', '.join(map(str, sizes))}",
                                  reply_markup=kb_)
    await callback.answer()


order_regex = "order_([^_]*)_([^_]*)_create"


@dp.callback_query_handler(regexp=order_regex)
async def order_choose_size(callback: types.CallbackQuery):
    asyncio.create_task(callback.answer())
    brand, model = re.search(order_regex, callback.data).groups()
    sizes = await db.get_stock_size(brand, model)

    msg_txt = f"""
    Выберите размер кроссовок {brand} {model}
    """
    kb_ = kb.create_sizes_ikb(sizes, brand, model)

    await callback.message.answer(msg_txt, reply_markup=kb_)


sizes_regex = 'order_([^_]*)_([^_]*)_([^_]*)_assortment'


@dp.callback_query_handler(regexp=sizes_regex)
async def order_model(callback: types.CallbackQuery):
    asyncio.create_task(callback.message.delete())
    asyncio.create_task(callback.answer())

    brand, model, size = re.search(sizes_regex, callback.data).groups()

    order_id = await db.create_order(callback.from_user.id, brand, model, size)
    msg_txt = f"""<b>Заказ №{order_id} успешно создан!</b>\n\n<b>Детали заказа:</b>
<em>Бренд:</em> {brand}
<em>Модель:</em> {model}
<em>Размер:</em> {size}
    """

    await callback.message.answer(msg_txt)
