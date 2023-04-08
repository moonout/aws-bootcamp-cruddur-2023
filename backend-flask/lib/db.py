import os

from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

connection_url = os.getenv("CONNECTION_URL")
db_name = os.getenv("DB_NAME")
pool = ConnectionPool(f"{connection_url}/{db_name}", kwargs={"row_factory": dict_row})


def _query(sql, params=None, without_return=False):
    params = params or {}
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            if without_return:
                return None
            return cursor.fetchall()


def query(sql, params=None):
    _query(sql, params, without_return=True)


def query_one(sql, params=None):
    result = _query(sql, params)
    return result[0] if result else None


def query_all(sql, params=None):
    result = _query(sql, params)
    return result
