import asyncpg
from . import config

import logging
from typing import Tuple
import collections.abc


async def create_connection():
    try:
        return await asyncpg.connect(database=config.PG_DBNAME, host=config.PG_HOST,
                                     user=config.PG_USER, password=config.PG_PASSWORD,
                                     port=config.PG_PORT)
    except (Exception, asyncpg.ConnectionFailureError) as error:
        logging.info(f"Error while connecting to database: {error}")
        raise error


def connect_to_db(coroutine):
    """ Decorator, connecting to db and closing connection after queries
    """

    async def wrapper(*args, **kwargs):
        conn = await create_connection()
        result = await coroutine(conn, *args, **kwargs)
        await conn.close()
        return result

    return wrapper


@connect_to_db
async def insert_many(conn: asyncpg.Connection,
                      table_name: str,
                      data: Tuple[Tuple],
                      specified_cols: tuple = None):
    specified_cols_str = ""
    if specified_cols:
        specified_cols_str = f"({', '.join(specified_cols)})"

    await conn.executemany(f'INSERT INTO {table_name} {specified_cols_str} VALUES ({_form_query_values(data[0])});',
                           data)


@connect_to_db
async def insert(conn: asyncpg.Connection,
                 table_name: str,
                 data: Tuple,
                 specified_cols: tuple = None):
    specified_cols_str = ""
    if specified_cols:
        specified_cols_str = f"({', '.join(specified_cols)})"

    await conn.execute(f"INSERT INTO {table_name}{specified_cols_str} VALUES ({_form_query_values(len(data))})",
                       *data)


@connect_to_db
async def select(conn: asyncpg.Connection,
                 table_name: str,
                 target: str = '*',
                 caption: str = "",
                 data: tuple = None):
    if data:
        return await conn.fetch(f"SELECT {target} FROM {table_name} {caption}", *data)
    return await conn.fetch(f"SELECT {target} FROM {table_name} {caption}")


def _form_query_values(n):
    if type(n) is int:
        return ", ".join([f'${el}' for el in range(1, n + 1)])
    elif isinstance(n, collections.abc.Collection):
        n = len(n)
        return _form_query_values(n)
