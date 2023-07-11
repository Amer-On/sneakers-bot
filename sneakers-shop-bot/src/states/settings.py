from aiogram.dispatcher.filters.state import StatesGroup, State


class SettingsStates(StatesGroup):
    nominal = State()
    phone_number = State()
    address = State()
    payment_method = State()
