from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    add_admin = State()
