from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from ..messages import commands


def form_delete_message_kb(additional_messages_to_delete: int = 0):
    return InlineKeyboardMarkup().add(
        form_delete_message_button(additional_messages_to_delete)
    )


def form_delete_message_button(additional_messages_to_delete: int = 0, text: str = commands.delete_message):
    callback_data = f"delete_message_{additional_messages_to_delete}"
    return InlineKeyboardButton(text, callback_data=callback_data)


remove_kb_button = InlineKeyboardButton(commands.remove_keyboard, callback_data="remove_keyboard")

back_kb = ReplyKeyboardMarkup().add(KeyboardButton(commands.back))
