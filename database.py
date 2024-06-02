from flask import g
from functools import wraps
import psycopg2
from settings import DATABASE


def db_connect(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        g.db_conn = psycopg2.connect(**DATABASE)
        g.db_conn.autocommit = True

        try:
            return func(*args, **kwargs)
        finally:
            g.db_conn.close()

    return wrapper
