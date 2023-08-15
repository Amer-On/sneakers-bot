from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from src.messages.commands import contact_method_callback_data
from src.messages import commands

payment_method = InlineKeyboardMarkup()

contact_methods_meta = {
    'Как хотите!)': 'any',
    'Телеграм': 'telegram',
    'Позвоните мне': 'phone',
    'WhatsApp': 'whatsapp'
}

contact_methods_meta_reversed = {v: k for k, v in contact_methods_meta.items()}

for method, method_type in contact_methods_meta.items():
    payment_method.add(InlineKeyboardButton(method, callback_data=contact_method_callback_data(method_type)))


payment_methods_meta = {
    'Наличными при получении💵': 'payment_cash',
    'Переводом при получении🔛': 'payment_transfer',
    'Переводом по предоплате (скидка 5%)🤑': 'payment_prepayment',
}


payment_methods_meta_reversed = {v: k for k, v in payment_methods_meta.items()}

payment_types = InlineKeyboardMarkup()
for method, method_type in payment_methods_meta.items():
    payment_types.add(InlineKeyboardButton(method, callback_data=method_type))


# payment_types.add(InlineKeyboardButton('Наличными при получении💵', callback_data='payment_cash'))
# payment_types.add(InlineKeyboardButton('Переводом при получении🔛', callback_data='payment_transfer'))
# payment_types.add(InlineKeyboardButton('Переводом по предоплате (скидка 5%)🤑', callback_data='payment_prepayment'))


# payment_method.add(InlineKeyboardButton(commands.change_phone, callback_data='settings_contact_back'))


cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.cancel))

change_name = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.change_name))

change_phone = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.change_phone))

change_contact_method = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.change_contact_method))

change_address = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.change_address))

change_payment_method = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(commands.change_payment_method))


confirm_settings = InlineKeyboardMarkup().add(InlineKeyboardButton('Подтвердить ✅', callback_data='confirm_settings'))
confirm_settings.add(InlineKeyboardButton('Пройти регистрацию заново ↩️', callback_data='restart_registration'))
confirm_settings.add(InlineKeyboardButton('Отменить регистрацию ❌', callback_data='cancel_registration'))
