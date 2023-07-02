from contextlib import suppress

from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from aiogram.types.message import ContentType

from src import messages
from src.misc import bot


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
