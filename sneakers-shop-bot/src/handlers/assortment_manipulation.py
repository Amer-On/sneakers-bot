import logging
import re
from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

import db
from src.misc import dp
from src.modules.bot_helpers import unknown_message_reply, remove_reply_keyboard
from src.states import AssortmentStates
from src import keyboards as kb


@dp.message_handler(lambda message: message.text == 'Назад',
                    state=AssortmentStates)
async def back_handler(message: types.Message, state: FSMContext):
    await message.answer("Действие успешно завершено", reply_markup=kb.menu)
    await state.finish()


@dp.message_handler(lambda message: message.text == 'Отмена',
                    state=AssortmentStates)
async def back_handler(message: types.Message, state: FSMContext):
    await message.answer("Действие отменено", reply_markup=kb.menu)
    await state.finish()


@dp.message_handler(commands='add_brand')
async def add_brand_cmd(message: types.Message):
    if await db.is_admin(message.from_user.id):
        await message.answer("Напишите бренд, который хотите добавить", reply_markup=kb.back_kb)
        await AssortmentStates.add_brand.set()
    else:
        await unknown_message_reply(message)


@dp.message_handler(state=AssortmentStates.add_brand)
async def add_brand(message: types.Message, state: FSMContext):
    brand = message.text
    await db.add_brand(brand)
    await message.answer("Бренд успешно добавлен")


@dp.message_handler(commands='add_model')
async def add_model_cmd(message: types.Message):
    if await db.is_admin(message.from_user.id):
        brands = await db.get_brands()
        kb_ = kb.create_brands_ikb(brands, manipulation=True)
        # await AssortmentStates.add_model_brand.set()
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


@dp.message_handler(commands='add_photos')
async def add_photos_cmd(message: types.Message):
    if await db.is_admin(message.from_user.id):
        brands = await db.get_brands()
        kb_ = kb.create_brands_ikb(brands, manipulation=True)
        await AssortmentStates.add_photos_brand.set()
        await message.answer("Выберите фирму кроссовок", reply_markup=kb_)
    else:
        await unknown_message_reply(message)


@dp.message_handler(commands='add_price')
async def add_price_cmd(message: types.Message):
    if await db.is_admin(message.from_user.id):
        brands = await db.get_brands()
        kb_ = kb.create_prices_ikb(brands)
        await AssortmentStates.add_price.set()
        await remove_reply_keyboard(message.from_user.id)
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


@dp.message_handler(commands='add_stock')
async def add_stock_cmd(message: types.Message, state: FSMContext):
    if await db.is_admin(message.from_user.id):
        brands = await db.get_brands()

        # kb_ = kb.create_brands_ikb(brands, manipulation=True)
        kb_ = kb.create_brands_stock_ikb(brands)
        # await AssortmentStates.add_stock.set()
        await message.answer("Выберите фирму кроссовок", reply_markup=kb_)
    else:
        await unknown_message_reply(message)


brand_regex = "choose_([^_]*)_assortment"


@dp.callback_query_handler(regexp=brand_regex, state=AssortmentStates.add_price)
async def add_price_choose_model(callback: types.CallbackQuery):
    brand = re.search(brand_regex, callback.data).group(1)
    models = tuple(el[1] for el in await db.get_models(brand))
    kb_ = kb.create_models_ikb(brand, models)
    await callback.message.answer("Выбери модель, для которой хочешь добавить/изменить цену", reply_markup=kb_)
    await callback.answer()


@dp.callback_query_handler(regexp=brand_regex, state=AssortmentStates.add_stock)
async def add_stock_choose_model(callback: types.CallbackQuery):
    brand = re.search(brand_regex, callback.data).group(1)
    models = tuple(el[1] for el in await db.get_models(brand))
    kb_ = kb.create_models_ikb(brand, models)
    await callback.message.answer("Выбери модель, для которой хочешь добавить ассортимент", reply_markup=kb_)
    await callback.answer()


stock_brand_regex = "update_([^_]*)_stock"


@dp.callback_query_handler(regexp=stock_brand_regex)
async def add_stock_brand(callback: types.CallbackQuery):
    brand = re.search(stock_brand_regex, callback.data).group(1)
    models = tuple(el[1] for el in await db.get_models(brand))
    kb_ = kb.create_models_stock_ikb(brand, models)
    await callback.message.answer("Выбери модель, для которой хочешь добавить сток", reply_markup=kb_)
    await callback.answer()


model_regex = "get_([^_]*)_([^_]*)_assortment"

stock_model_regex = "update_([^_]*)_([^_]*)_stock"


@dp.callback_query_handler(regexp=stock_model_regex)
async def add_stock_model(callback: types.CallbackQuery, state: FSMContext):
    brand, model = re.search(stock_model_regex, callback.data).groups()
    async with state.proxy() as data:
        data['brand'] = brand
        data['model'] = model

    await AssortmentStates.add_stock_manipulation.set()
    await callback.message.answer(
        "Введите размер и количество поставленных кроссовок через пробел (размер количество)\n"
        "Если хотите уменьшить ассортимент, введите отрицательное количество", reply_markup=kb.back_kb)
    await callback.answer()


@dp.callback_query_handler(regexp=model_regex, state=AssortmentStates.add_price)
async def add_price_model(callback: types.CallbackQuery, state: FSMContext):
    brand, model = re.search(model_regex, callback.data).groups()
    async with state.proxy() as data:
        data['brand'] = brand
        data['model'] = model

    await AssortmentStates.add_price_manipulation.set()
    await callback.message.answer("Введите стоимость выбранной модели (число)\n", reply_markup=kb.back_kb)
    await callback.answer()


@dp.message_handler(state=AssortmentStates.add_price_manipulation)
async def add_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        brand = data['brand']
        model = data['model']

    price = message.text

    try:
        price = int(price)
    except:
        await message.answer("Пожалуйста введите число")
        return

    await db.add_price(brand, model, price)
    await state.finish()
    await message.answer("Стоимость успешно добавлена", reply_markup=kb.menu)


@dp.message_handler(state=AssortmentStates.add_stock_manipulation)
async def add_stock(message: types.Message, state: FSMContext):
    try:
        size, amount = map(int, message.text.split())
        async with state.proxy() as data:
            brand = data['brand']
            model = data['model']
        await db.add_stock(brand, model, size, amount)
        await message.answer("Запас увеличен")
    except Exception as e:
        print(e)
        await message.answer("Некорректные данные")


@dp.message_handler(state=AssortmentStates.add_photos)
async def photos_addition_finish(message: types.Message):
    await message.answer("Пожалуйста отправьте фото или нажмите кнопку назад")


@dp.callback_query_handler(regexp=brand_regex, state=AssortmentStates.add_photos_brand)
async def add_photo_model_query(callback: types.CallbackQuery, state: FSMContext):
    brand = re.search(brand_regex, callback.data).group(1)
    models = tuple(el[1] for el in await db.get_models(brand))
    await AssortmentStates.add_photos_model.set()
    kb_ = kb.create_models_ikb(brand, models)
    await callback.message.answer("Выбери модель, для которой хочешь добавить фотографии", reply_markup=kb_)
    await callback.answer()


@dp.callback_query_handler(regexp=brand_regex)
async def add_model_query(callback: types.CallbackQuery, state: FSMContext):
    brand = re.search(brand_regex, callback.data).group(1)
    async with state.proxy() as data:
        data['brand'] = brand

    await callback.message.answer(f"Введите название модели бренда {brand}", reply_markup=kb.back_kb)
    await AssortmentStates.add_model.set()
    await callback.answer()


@dp.callback_query_handler(regexp=model_regex, state=AssortmentStates.add_photos_model)
async def add_model_photos(callback: types.CallbackQuery, state: FSMContext):
    brand, model = re.search(model_regex, callback.data).groups()
    async with state.proxy() as data:
        data['brand'] = brand
        data['model'] = model

    await callback.message.answer("Отправьте фотографии, которые хотите прикрепить", reply_markup=kb.back_kb)
    await callback.answer()
    await AssortmentStates.add_photos.set()
