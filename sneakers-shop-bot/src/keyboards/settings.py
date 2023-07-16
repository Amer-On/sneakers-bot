from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from src.messages.commands import contact_method_callback_data

payment_method = InlineKeyboardMarkup()

payment_methods_meta = {
    'Как хотите!)': 'any',
    'Телеграм': 'telegram',
    'Позвоните мне': 'phone',
    'WhatsApp': 'whatsapp'
}

for method, method_type in payment_methods_meta.items():
    payment_method.add(InlineKeyboardButton(method, callback_data=contact_method_callback_data(method_type)))
