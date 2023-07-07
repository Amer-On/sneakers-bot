from aiogram.dispatcher.filters.state import StatesGroup, State


class AssortmentStates(StatesGroup):
    add_brand = State()
    add_model = State()
    add_model_brand = State()

    add_photos_brand = State()
    add_photos_model = State()
    add_photos = State()

    add_stock = State()
    add_stock_manipulation = State()
