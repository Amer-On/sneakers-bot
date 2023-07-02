callbacks_and_commands = {
    "assortment_search": "Поиск по ассортименту",
    "assortment_navigation": "Выбрать из ассортимента",
}

delete_message = "Закрыть ❌"
remove_keyboard = "Убрать клавиатуру"


# CALLBACK DATA FORMERS
def search_callback_data(name: str):
    return f"find_{name}"


def navigation_brands_callback_data(brand: str):
    return f"get_{brand}_assortment"


def manipulation_brands_callback_data(brand: str):
    return f"choose_{brand}_assortment"


def navigation_models_callback_data(model: str, brand: str):
    return f"get_{brand}_{model}_assortment"
