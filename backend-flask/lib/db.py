import os

from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

connection_url = os.getenv("CONNECTION_URL")

pool = ConnectionPool(connection_url, kwargs={"row_factory": dict_row})
