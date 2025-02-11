import sqlite3
import random

# Подключаемся к базе
conn = sqlite3.connect("photos.db")
cursor = conn.cursor()

# Создаём таблицу, если её нет
cursor.execute("""
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT NOT NULL,
    user_id INTEGER NOT NULL
)
""")
conn.commit()


def add_photo(file_id: str, user_id: int):
    """Добавляет фото в базу данных с привязкой к user_id"""
    cursor.execute("INSERT INTO photos (file_id, user_id) VALUES (?, ?)", (file_id, user_id))
    conn.commit()


def get_random_photo(user_id: int):
    """Получает случайное фото для конкретного user_id"""
    cursor.execute("SELECT file_id FROM photos WHERE user_id = ?", (user_id,))
    photos = cursor.fetchall()

    if photos:
        return random.choice(photos)[0]  # Возвращаем случайное фото
    return None  # Если фото нет


def clear_photos():
    """Очищает базу (удаляет все фото)"""
    cursor.execute("DELETE FROM photos")
    conn.commit()
