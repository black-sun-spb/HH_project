import psycopg2
from psycopg2.extensions import connection

def get_connection() -> connection:
    return psycopg2.connect(
        dbname='hh_db',
        user='postgres',
        password='20012010',
        host='localhost',
        port='5432'
    )
