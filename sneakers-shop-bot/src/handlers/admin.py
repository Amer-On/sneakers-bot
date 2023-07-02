from aiogram.dispatcher import FSMContext

from src.misc import dp
from src import states
from aiogram import types
import db
from src.modules.bot_helpers import unknown_message_reply


@dp.message_handler(commands='get_id')
async def get_id(message: types.Message):
    await message.answer(message.from_user.id)


@dp.message_handler(commands='add_admin', state='*')
async def add_admin(message: types.Message):
    if await db.is_admin(message.from_user.id):
        await message.answer("Перешлите любое сообщение администратора, которого вы хотите добавить")
        await states.AdminStates.add_admin.set()
    else:
        await unknown_message_reply(message)


@dp.message_handler(state=states.AdminStates.add_admin)
async def add_admin(message: types.Message, state: FSMContext):
    user_id = message.forward_from.id
    if not await db.add_user(user_id, is_admin=True):
        await db.make_admin(user_id)
    await message.answer(f"User {user_id} is admin")
    await state.finish()


@dp.message_handler(commands='get_admins', state='*')
async def get_admins(message: types.Message):
    if await db.is_admin(message.from_user.id):
        admins = await db.get_admins()
        await message.answer("<b>Администраторы:</b>\n" + '\n'.join(map(str, admins)))
    else:
        await unknown_message_reply(message)
