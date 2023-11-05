import asyncpg

from ..general import connect_to_db, insert
from . import models

TABLE_NAME = 'photos'


@connect_to_db
async def create_photos_table(conn: asyncpg.Connection):
    await conn.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    brand VARCHAR(50),
    model VARCHAR(50),
    photo_id VARCHAR(100),
    FOREIGN KEY (brand, model) REFERENCES {models.TABLE_NAME}(brand, model),
    CONSTRAINT pk_{TABLE_NAME} PRIMARY KEY ( brand, model, photo_id )
    );""")


@connect_to_db
async def get_photos(conn: asyncpg.Connection, brand: str, model: str):
    res = await conn.fetch(f"SELECT (photo_id) FROM {TABLE_NAME} WHERE brand = $1 AND model = $2", brand, model)
    return tuple(el[0] for el in res)


async def add_photo(brand: str, model: str, photo_id: str):
    await insert(TABLE_NAME, (brand, model, photo_id))
