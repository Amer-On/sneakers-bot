from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from ..messages import commands


# menu = InlineKeyboardMarkup()
# for callback, command in commands.callbacks_and_commands:
#     menu.add(
#         InlineKeyboardButton(command, callback_data=callback)
#     )


menu = ReplyKeyboardMarkup(resize_keyboard=True)
for command in commands.callbacks_and_commands.values():
    menu.add(command)
