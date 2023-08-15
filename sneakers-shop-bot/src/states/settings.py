from aiogram.dispatcher.filters.state import StatesGroup, State


class SettingsStates(StatesGroup):
    nominal = State()
    phone_number = State()
    contact_method = State()
    address = State()
    payment_method = State()
    confirm = State()
