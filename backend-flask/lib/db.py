import os

from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

connection_url = os.getenv("CONNECTION_URL")
db_name = os.getenv("DB_NAME")
pool = ConnectionPool(f"{connection_url}/{db_name}", kwargs={"row_factory": dict_row})
