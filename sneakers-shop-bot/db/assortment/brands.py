import asyncpg

from ..general import connect_to_db, insert

TABLE_NAME = 'brands'


@connect_to_db
async def create_brands_table(conn: asyncpg.Connection):
    await conn.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    name VARCHAR(15) PRIMARY KEY
    )""")


@connect_to_db
async def get_brands(conn: asyncpg.Connection):
    res = await conn.fetch(f"SELECT name FROM {TABLE_NAME}")
    return tuple(el[0] for el in res)


async def add_brand(firm: str):
    await insert(TABLE_NAME, (firm, ))
