import logging

from database.db import get_connection


def save_metadata(filename: str, original_name: str, size: int, file_type: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                sql = """
                        INSERT INTO images (filename, original_name, size, file_type)
                        VALUES (%s, %s, %s, %s);
                        """
                cursor.execute(sql, (filename, original_name, size, file_type))
                conn.commit()
                logging.info(f'БД:Метаданные для {filename} сохранены')
            except Exception as e:
                conn.rollback()
                logging.error(e)
                raise


def get_images(per_page: int, offset: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT id,filename,original_name,size,upload_time,file_type 
                    FROM images
                    ORDER BY upload_time DESC
                    LIMIT %s OFFSET %s;
                    ''', (per_page, offset))
                rows = cur.fetchall()
        return rows
    except Exception as e:
        logging.error('НЕ смогли вытащить данные из бд.')
        raise


def get_count_images():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM images;")
                total = cur.fetchone()[0]
        return total
    except Exception:
        logging.error('НЕ смогли вытащить данные из бд.')
        raise
