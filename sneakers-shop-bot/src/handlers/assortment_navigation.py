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

    photos = await db.get_photos(brand, model)
    media = types.MediaGroup()
    for el in photos:
        media.attach_photo(photo=el)

    await callback.message.answer_media_group(media)
    await callback.message.answer(f"{brand} {model}\nAvailable sizes: 36-40",
                                  reply_markup=kb.form_delete_message_button(len(photos)))
    await callback.answer()
