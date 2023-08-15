import asyncio
import logging
from contextlib import suppress

from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from aiogram.types.message import ContentType

from src import messages
from src.misc import bot
from src.keyboards.settings import contact_methods_meta_reversed, payment_methods_meta_reversed
import db


async def update_text(message: types.Message, text, keyboard=None):
    with suppress(MessageNotModified):
        if message.content_type == ContentType.TEXT:
            await message.edit_text(text, reply_markup=keyboard)
        else:
            await message.edit_caption(text, reply_markup=keyboard)


async def remove_reply_keyboard(chat_id: int,
                                message_text: str = "o"):
    """ Removes reply keyboard

        Sends a new message with meaningless text and aiogram.types.ReplyKeyboardRemove
            as a reply_markup parameter to the send_message method, then deletes the message
    """
    msg = await bot.send_message(chat_id,
                                 message_text,
                                 reply_markup=types.ReplyKeyboardRemove(),
                                 parse_mode="MarkdownV2")
    await msg.delete()


async def unknown_message_reply(message: types.Message):
    await message.answer(messages.unknown)


async def notify_admins(message_text: str):
    admins = await db.get_admins()
    for admin in admins:
        asyncio.create_task(bot.send_message(admin, message_text))
    logging.info("Admins notified")


async def delete_messages(user_id: int, message_id: int, to_remove: int = 1):
    for i in range(to_remove):
        await bot.delete_message(user_id, message_id - i)


async def remove_keyboard(message: types.Message, message_text: str | None = None):
    if not message_text:
        message_text = message.text
    await update_text(message, message_text, keyboard=None)


def prepare_user_settings(nominal: str, phone: str, contact_method: str, address: str, payment_method: str):
    return f'''Настройки пользователя ⚙️ 

Имя: <em>{nominal}</em>
Номер телефона: <em>{phone}</em>
Метод связи: <em>{contact_methods_meta_reversed[contact_method]}</em>
Адрес: <em>{address}</em>
Метод оплаты: <em>{payment_methods_meta_reversed[f'payment_{payment_method}']}</em>
'''

