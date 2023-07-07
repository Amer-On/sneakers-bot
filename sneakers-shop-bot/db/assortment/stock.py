import asyncpg

from ..general import connect_to_db, insert
from . import models

TABLE_NAME = 'stock'


@connect_to_db
async def create_stock_table(conn: asyncpg.Connection):
    await conn.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    brand VARCHAR(15),
    model VARCHAR(15),
    size INT,
    amount INT DEFAULT 100,
    FOREIGN KEY (brand, model) REFERENCES {models.TABLE_NAME}(brand, model),
    CONSTRAINT pk_{TABLE_NAME} PRIMARY KEY ( brand, model, size )
    );""")


@connect_to_db
async def get_stock_size(conn: asyncpg.Connection, brand: str, model: str):
    res = await conn.fetch(f"SELECT (size) FROM {TABLE_NAME} WHERE brand = $1 AND model = $2 AND amount > 0", brand, model)
    return tuple(el[0] for el in res)


async def add_stock(brand: str, model: str, size: int, amount: int = 100):
    await insert(TABLE_NAME, (brand, model, size, amount))


@connect_to_db
async def get_brand_models_by_size(conn: asyncpg.Connection, brand: str, size: int):
    res = conn.fetch(f"SELECT * FROM {TABLE_NAME} WHERE brand = $1 AND size = $2", brand, size)
    return tuple(el[0] for el in res)

