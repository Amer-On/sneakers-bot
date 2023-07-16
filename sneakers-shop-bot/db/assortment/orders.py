from ..general import *
from ..users.conf import TABLE_NAME as USERS_TABLE_NAME
from .models import TABLE_NAME as MODELS_TABLE_NAME

TABLE_NAME = 'orders'


@connect_to_db
async def create_orders_statuses(conn: asyncpg.Connection):
    await conn.execute('DROP TABLE IF EXISTS orders_statuses CASCADE')
    await conn.execute(
        f'''
        CREATE TABLE IF NOT EXISTS orders_statuses (
        status VARCHAR PRIMARY KEY
        )''')
    # await insert_many('orders_statuses', (('MODERATION'), ('APPROVED'), ('CANCELED')), )
    await conn.execute("INSERT INTO orders_statuses (status) VALUES ($1)", 'MODERATION')
    await conn.execute("INSERT INTO orders_statuses (status) VALUES ($1)", 'APPROVED')
    await conn.execute("INSERT INTO orders_statuses (status) VALUES ($1)", 'CANCELED')
    # await conn.executemany("INSERT INTO orders_statuses (status) VALUES ($1)", (('MODERATION'), ('APPROVED'), ('CANCELED')))


@connect_to_db
async def create_orders_table(conn: asyncpg.Connection):
    await conn.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id BIGINT,
        order_id SERIAL,
        
        brand VARCHAR,
        model VARCHAR,
        size INT,
        amount INT DEFAULT 1,
        status VARCHAR DEFAULT 'MODERATION',
        
        FOREIGN KEY (status) REFERENCES orders_statuses(status),
        FOREIGN KEY (brand, model) REFERENCES {MODELS_TABLE_NAME}(brand, model),
        FOREIGN KEY (user_id) REFERENCES {USERS_TABLE_NAME}(user_id),
        CONSTRAINT pk_{TABLE_NAME} PRIMARY KEY ( order_id )
        )''')


@connect_to_db
async def create_order(conn: asyncpg.Connection, user_id: int, brand: str, model: str, size: int, amount: int = 1):
    return await conn.fetchval(
        f"INSERT INTO {TABLE_NAME} (user_id, brand, model, size, amount) VALUES ($1, $2, $3, $4, $5) RETURNING order_id",
        user_id, brand, model, int(size), amount)


@connect_to_db
async def get_order(conn: asyncpg.Connection, order_id: int):
    return await conn.fetchrow(f"SELECT * FROM {TABLE_NAME} WHERE $1 = order_id", order_id)
