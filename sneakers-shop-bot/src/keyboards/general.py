from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from ..messages import commands


def form_delete_message_button(additional_messages_to_delete: int = 0):
    callback_data = f"delete_message_{additional_messages_to_delete}"
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(commands.delete_message, callback_data=callback_data)
    )


remove_kb_button = InlineKeyboardButton(commands.remove_keyboard, callback_data="remove_keyboard")

back_kb = ReplyKeyboardMarkup().add(KeyboardButton("Назад"))

# delete_message_ikb = InlineKeyboardMarkup().add(
#     delete_message_button
# )
