import sqlite3
import random


# Создание базы данных
def init_db():
    conn = sqlite3.connect("photos.db")  # Файл базы
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()


# Добавление фото в базу
def add_photo(file_id):
    conn = sqlite3.connect("photos.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO photos (file_id) VALUES (?)", (file_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Если фото уже есть, просто игнорим ошибку
    finally:
        conn.close()


# Получение рандомного фото
def get_random_photo():
    conn = sqlite3.connect("photos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM photos")
    photos = cursor.fetchall()
    conn.close()

    if photos:
        return random.choice(photos)[0]  # Выбираем рандомное фото
    return None


# Инициализация базы при запуске
init_db()