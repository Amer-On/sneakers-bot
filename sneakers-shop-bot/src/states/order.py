from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderStates(StatesGroup):
    pass


class RefundStates(StatesGroup):
    refund = State()
