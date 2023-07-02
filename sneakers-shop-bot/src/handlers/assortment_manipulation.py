import logging
import re
from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

import db
from src.misc import dp
from src.modules.bot_helpers import unknown_message_reply
from src.states import AssortmentStates
from src import keyboards as kb


@dp.message_handler(commands='add_model')
async def add_model_cmd(message: types.Message):
    if await db.is_admin(message.from_user.id):
        brands = await db.get_brands()
        kb_ = kb.create_brands_ikb(brands, manipulation=True)
        await AssortmentStates.add_model_brand.set()
        await message.answer("Выберите фирму кроссовок", reply_markup=kb_)
    else:
        await unknown_message_reply(message)


@dp.message_handler(state=AssortmentStates.add_model)
async def add_model(message: types.Message, state: FSMContext):
    model = message.text

    async with state.proxy() as data:
        brand = data['brand']

    try:
        await db.add_model(brand, model)
        await message.answer("Модель успешно добавлена")
    except:
        await message.answer("Произошла неизвестная ошибка при добавлении модели")
    await state.finish()


@dp.message_handler(commands='add_photos')
async def add_photos_cmd(message):
    if await db.is_admin(message.from_user.id):
        brands = await db.get_brands()
        kb_ = kb.create_brands_ikb(brands, manipulation=True)
        await AssortmentStates.add_photos_brand.set()
        await message.answer("Выберите фирму кроссовок", reply_markup=kb_)
    else:
        await unknown_message_reply(message)


@dp.message_handler(state=AssortmentStates.add_photos, content_types=['photo'])
async def add_photos(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    async with state.proxy() as data:
        try:
            await db.add_photo(data['brand'], data['model'], photo_id)
            logging.debug(f"Photo for {data['brand']} {data['model']} added")
        except Exception as e:
            logging.debug(f"Some exception {e} occurred while saving photo")


@dp.message_handler(lambda message: message.text == 'Назад', state=AssortmentStates.add_photos)
async def photos_addition_finish(message: types.Message, state: FSMContext):
    await message.answer("Добавление фото завершено", reply_markup=kb.menu)
    await state.finish()


@dp.message_handler(state=AssortmentStates.add_photos)
async def photos_addition_finish(message: types.Message):
    await message.answer("Пожалуйста отправьте фото или нажмите кнопку назад")


brand_regex = "choose_([^_]*)_assortment"


@dp.callback_query_handler(regexp=brand_regex, state=AssortmentStates.add_photos_brand)
async def add_photo_model_query(callback: types.CallbackQuery, state: FSMContext):
    brand = re.search(brand_regex, callback.data).group(1)
    models = tuple(el[1] for el in await db.get_models(brand))
    await AssortmentStates.add_photos_model.set()
    kb_ = kb.create_models_ikb(brand, models)
    await callback.message.answer("Выбери модель, для которой хочешь добавить фотографии", reply_markup=kb_)
    await callback.answer()


@dp.callback_query_handler(regexp=brand_regex, state=AssortmentStates.add_model_brand)
async def add_model_query(callback: types.CallbackQuery, state: FSMContext):
    brand = re.search(brand_regex, callback.data).group(1)
    async with state.proxy() as data:
        data['brand'] = brand

    await callback.message.answer(f"Введите название модели бренда {brand}")
    await AssortmentStates.add_model.set()
    await callback.answer()


model_regex = "get_([^_]*)_([^_]*)_assortment"


@dp.callback_query_handler(regexp=model_regex, state=AssortmentStates.add_photos_model)
async def add_model_photos(callback: types.CallbackQuery, state: FSMContext):
    brand, model = re.search(model_regex, callback.data).groups()
    async with state.proxy() as data:
        data['brand'] = brand
        data['model'] = model

    await callback.message.answer("Отправьте фотографии, которые хотите прикрепить", reply_markup=kb.back_kb)
    await callback.answer()
    await AssortmentStates.add_photos.set()

