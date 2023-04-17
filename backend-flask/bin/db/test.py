#!/usr/bin/env python3

import psycopg
import os

# import sys

# if len(sys.argv) == 2 and sys.argv[1] == "prod":
#     connection_url = os.environ["PROD_CONNECTION_URL"]
# else:
#     connection_url = os.getenv("LOCAL_CONNECTION_URL")
connection_url = os.getenv("CONNECTION_URL")
conn = None
try:
    print("attempting connection")
    conn = psycopg.connect(connection_url)
    print("Connection successful!")
except psycopg.Error as e:
    print("Unable to connect to the database:", e)
finally:
    if conn is not None:
        conn.close()
