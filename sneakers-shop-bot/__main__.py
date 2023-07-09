import asyncio

from src.misc import executor
import __init__
import db.users


async def on_startup():
    await db.users.create_table()
    await db.create_brands_table()
    await db.create_models_table()
    await db.create_photos_table()
    await db.create_stock_table()
    await db.create_orders_statuses()
    await db.create_orders_table()


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(on_startup())
    executor.start_polling()


if __name__ == "__main__":
    main()
