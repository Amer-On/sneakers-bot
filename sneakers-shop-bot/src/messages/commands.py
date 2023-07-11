callbacks_and_commands = {
    # "assortment_search": "Поиск по ассортименту",
    "assortment_navigation": "Посмотреть ассортимент",
    "settings": "Изменить настройки"
}

delete_message = "Закрыть ❌"
remove_keyboard = "Убрать клавиатуру"
order = "Заказать"
back = 'Назад'
cancel = 'Отмена'


# CALLBACK DATA FORMERS
def search_callback_data(name: str):
    return f"find_{name}"


def navigation_brands_callback_data(brand: str):
    return f"get_{brand}_assortment"


def manipulation_brands_callback_data(brand: str):
    return f"choose_{brand}_assortment"


def stock_brands_callback_data(brand: str):
    return f"update_{brand}_stock"


def stock_models_callback_data(model: str, brand: str):
    return f"update_{brand}_{model}_stock"


def navigation_models_callback_data(model: str, brand: str):
    return f"get_{brand}_{model}_assortment"


def order_create_callback_data(brand: str, model: str):
    return f"order_{brand}_{model}_create"


def sizes_callback_data(size: int, brand: str, model: str):
    return f"order_{brand}_{model}_{size}_assortment"
