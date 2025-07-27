import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database():
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "hh_db")

    conn = psycopg2.connect(
        dbname="postgres", user=user, password=password, host=host, port=port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    with conn.cursor() as cur:
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}';")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {dbname};")
            print(f"База данных {dbname} создана")
        else:
            print(f"База данных {dbname} уже существует")

    conn.close()
