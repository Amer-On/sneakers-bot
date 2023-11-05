import asyncpg

from ..general import connect_to_db, insert
from . import brands

TABLE_NAME = 'models'


@connect_to_db
async def create_models_table(conn: asyncpg.Connection):
    await conn.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    brand VARCHAR(50),
    model VARCHAR(50),
    FOREIGN KEY (brand) REFERENCES {brands.TABLE_NAME}(name),
    CONSTRAINT pk_{TABLE_NAME} PRIMARY KEY (brand, model)
    );""")


@connect_to_db
async def get_models(conn: asyncpg.Connection, brand: str):
    res = await conn.fetch(f"SELECT * FROM {TABLE_NAME} WHERE brand = $1", brand)
    return tuple(tuple(el) for el in res)


async def add_model(brand: str, model: str):
    await insert(TABLE_NAME, (brand, model), specified_cols=('brand', 'model'))
