from ..general import *
from .conf import TABLE_NAME


@connect_to_db
async def is_admin(conn: asyncpg.Connection, user_id: int):
    return await conn.fetchval("SELECT is_admin FROM users WHERE user_id = $1", user_id)


@connect_to_db
async def make_admin(conn: asyncpg.Connection, user_id: int):
    await conn.execute(f"UPDATE {TABLE_NAME} SET is_admin = TRUE WHERE user_id = $1", user_id)


@connect_to_db
async def add_user(conn: asyncpg.Connection,
                   user_id: int,
                   is_admin_: bool = False):
    await insert(conn, TABLE_NAME, data=(user_id, is_admin_))


@connect_to_db
async def get_admins(conn: asyncpg.Connection):
    res = await conn.fetch(f"SELECT user_id FROM {TABLE_NAME} WHERE is_admin = TRUE")
    return tuple(el[0] for el in res)
