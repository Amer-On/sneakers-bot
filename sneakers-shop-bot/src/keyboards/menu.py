from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from ..messages import commands


# menu = InlineKeyboardMarkup()
# for callback, command in commands.callbacks_and_commands:
#     menu.add(
#         InlineKeyboardButton(command, callback_data=callback)
#     )


menu = ReplyKeyboardMarkup()
for command in commands.callbacks_and_commands.values():
    menu.add(command)


payment_types = InlineKeyboardMarkup()
payment_types.add(InlineKeyboardButton('Наличными при получении💵', callback_data='payment_cash'))
payment_types.add(InlineKeyboardButton('Переводом при получении🔛', callback_data='payment_transfer'))
payment_types.add(InlineKeyboardButton('Переводом по предоплате (скидка 5%)🤑', callback_data='payment_prepayment'))
