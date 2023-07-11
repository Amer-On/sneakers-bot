import asyncpg

from ..general import connect_to_db, insert, _form_query_values

from . import conf

TABLE_NAME = "settings"


@connect_to_db
async def create_payment_methods_table(conn: asyncpg.Connection):
    await conn.execute("DROP TABLE IF EXISTS payment_method CASCADE")
    await conn.execute(f"""CREATE TABLE IF NOT EXISTS payment_method (
    payment VARCHAR,
    CONSTRAINT pk_payment_method PRIMARY KEY ( payment )
    );""")

    await conn.execute(f"INSERT INTO payment_method VALUES ($1)", 'cash')
    await conn.execute(f"INSERT INTO payment_method VALUES ($1)", 'transfer')
    await conn.execute(f"INSERT INTO payment_method VALUES ($1)", 'prepayment')


@connect_to_db
async def create_settings_table(conn: asyncpg.Connection):
    await conn.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    user_id INT,
    username VARCHAR,
    -- nominal - Имя пользователя
    nominal VARCHAR, 
    phone VARCHAR,
    address VARCHAR,
    payment_method VARCHAR,
    FOREIGN KEY (user_id) REFERENCES {conf.TABLE_NAME} (user_id),
    FOREIGN KEY (payment_method) REFERENCES payment_method (payment),
    CONSTRAINT pk_{TABLE_NAME} PRIMARY KEY ( user_id )
    );""")


async def add_user_settings(user_id: int,
                            username: str,
                            nominal: str,
                            phone: str,
                            address: str,
                            payment_method: str):
    await insert(TABLE_NAME, (user_id, username, nominal, phone, address, payment_method))


@connect_to_db
async def get_user_settings(conn: asyncpg.Connection, user_id: int):
    return await conn.fetchrow(f"SELECT * FROM {TABLE_NAME} WHERE user_id = $1", user_id)


@connect_to_db
async def update_user_settings(conn: asyncpg.Connection,
                               user_id: int,
                               nominal: str,
                               phone: str,
                               address: str,
                               payment_method: str):
    await conn.execute(f"UPDATE {TABLE_NAME} SET nominal = $2, phone = $3, address = $4, payment_method = $5 WHERE user_id = $1",
                       user_id, nominal, phone, address, payment_method)
