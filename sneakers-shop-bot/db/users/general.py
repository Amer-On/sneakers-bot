from ..general import *
from .conf import TABLE_NAME


@connect_to_db
async def create_table(conn: asyncpg.Connection):
    await conn.execute(
        f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (user_id BIGINT PRIMARY KEY, is_admin BOOl DEFAULT FALSE)")


async def add_user(user_id: int,
                   is_admin: bool = False):
    try:
        await insert(TABLE_NAME, (user_id, is_admin))
        return True
    except asyncpg.exceptions.UniqueViolationError as e:
        logging.error("USER IS ALREADY IN BASE")
    except:
        logging.error("Unknown error")
    return False
