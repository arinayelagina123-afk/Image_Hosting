from database.db import get_connection


def create_images():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(100) NOT NULL UNIQUE,
            original_name TEXT NOT NULL,
            size INTEGER NOT NULL,
            upload_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            file_type VARCHAR(4) NOT NULL
            );
            ''')
            conn.commit()
            return 'Таблица создана'
