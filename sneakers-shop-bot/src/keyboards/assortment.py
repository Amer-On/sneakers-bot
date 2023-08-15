from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from collections.abc import Collection
from typing import Callable
from ..messages import commands
from .general import form_delete_message_button

from src import messages

apply_registration = InlineKeyboardMarkup().add(
    InlineKeyboardButton(messages.apply_registration, callback_data='apply_registration'))


def create_search_ikb(data: Collection):
    ikb = InlineKeyboardMarkup()
    for el in data:
        ikb.add(InlineKeyboardButton(' '.join(el),
                                     callback_data=commands.navigation_models_callback_data(el[1], el[0])))
    return ikb


def create_models_ikb(brand: str, models: Collection[str]):
    return create_ikb(models, commands.navigation_models_callback_data, brand)


def create_prices_ikb(brands: Collection):
    return create_ikb(brands, commands.manipulation_brands_callback_data)


def create_brands_ikb(companies: Collection, manipulation: bool = False):
    if manipulation:
        return create_ikb(companies, commands.manipulation_brands_callback_data)
    return create_ikb(companies, commands.navigation_brands_callback_data)


def create_models_stock_ikb(brand: str, models: Collection[str]):
    return create_ikb(models, commands.stock_models_callback_data, brand)


def create_brands_stock_ikb(companies: Collection):
    return create_ikb(companies, commands.stock_brands_callback_data)


def create_sizes_ikb(sizes: Collection, brand, model):
    sizes_ikb = create_ikb(sizes, commands.sizes_callback_data, brand, model)
    sizes_ikb.add(form_delete_message_button(text=commands.cancel))
    return sizes_ikb


def create_order_ikb(brand: str, model: str, photos_amount: int):
    order_ikb = InlineKeyboardMarkup()
    order_ikb.add(
        InlineKeyboardButton(commands.order, callback_data=commands.order_create_callback_data(brand, model))
    )
    order_ikb.add(form_delete_message_button(photos_amount))
    return order_ikb


def create_ikb(data: Collection, callback_form_function: Callable, *args) -> InlineKeyboardMarkup:
    """ General function to form Inline Keyboards to navigate through assortment

    :param data: main data passed to function
    :type data: collections.Collection
    :param callback_form_function: function to form callback data
    :type callback_form_function: typing.Callable
    :param args: additional arguments
    :return: final inline keyboard
    :rtype: aiogram.types.InlineKeyboardMarkup
    """
    ikb = InlineKeyboardMarkup()
    for el in data:
        ikb.add(InlineKeyboardButton(el,
                                     callback_data=callback_form_function(el, *args)))
    return ikb
