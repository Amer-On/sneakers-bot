from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from collections.abc import Collection
from typing import Callable
from ..messages import commands


def create_models_ikb(brand: str, models: Collection[str]):
    return create_ikb(models, commands.navigation_models_callback_data, brand)


def create_brands_ikb(companies: Collection, manipulation: bool = False):
    if manipulation:
        return create_ikb(companies, commands.manipulation_brands_callback_data)
    return create_ikb(companies, commands.navigation_brands_callback_data)


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
