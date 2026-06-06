import os

import psycopg


def get_connection():
    return psycopg.connect(
        dbname='images_db',
        user="postgres",
        password="password",
        host="localhost",
        port="5435"
    )
