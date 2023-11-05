import asyncpg

from ..general import connect_to_db, insert
from .models import TABLE_NAME as MODELS_TABLE_NAME

TABLE_NAME = 'prices'


@connect_to_db
async def create_prices_table(conn: asyncpg.Connection):
    await conn.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    brand VARCHAR(50),
    model VARCHAR(50),
    price INT,
    FOREIGN KEY (brand, model) REFERENCES {MODELS_TABLE_NAME}(brand, model),
    CONSTRAINT pk_{TABLE_NAME} PRIMARY KEY ( brand, model )
    )""")


@connect_to_db
async def get_price(conn: asyncpg.Connection, brand: str, model: str):
    res = await conn.fetchval(f"SELECT price FROM {TABLE_NAME} WHERE brand = $1 AND model = $2", brand, model)
    return res


@connect_to_db
async def add_price(conn: asyncpg.Connection, brand: str, model: str, price: int):
    await conn.execute(
        f"UPDATE {TABLE_NAME} SET price = $3 WHERE brand = $1 AND model = $2",
        brand, model, price)
    await conn.execute(
        f"INSERT INTO {TABLE_NAME} VALUES ($1, $2, $3) ON CONFLICT DO NOTHING",
        brand, model, price)
