import os

import psycopg


def get_connection():# берет значения из переменных окружения для актуальности
    return psycopg.connect(
        dbname=os.environ.get("POSTGRES_DB", "images_db"),
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ.get("POSTGRES_PASSWORD", "password"),
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", "5435"),
    )