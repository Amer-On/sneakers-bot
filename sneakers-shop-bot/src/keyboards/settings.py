from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from src.messages.commands import contact_method_callback_data
from src.messages import commands

payment_method = InlineKeyboardMarkup()

payment_methods_meta = {
    'Как хотите!)': 'any',
    'Телеграм': 'telegram',
    'Позвоните мне': 'phone',
    'WhatsApp': 'whatsapp'
}

for method, method_type in payment_methods_meta.items():
    payment_method.add(InlineKeyboardButton(method, callback_data=contact_method_callback_data(method_type)))

# payment_method.add(InlineKeyboardButton(commands.change_phone, callback_data='settings_contact_back'))


cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.cancel))

change_name = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.change_name))

change_phone = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.change_phone))

change_contact_method = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.change_contact_method))

change_address = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.change_address))

change_payment_method = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.change_payment_method))
