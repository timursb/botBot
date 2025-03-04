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
    user_id INTEGER NOT NULL,
    album_name TEXT NOT NULL
)
""")
conn.commit()

def add_photo(file_id: str, user_id: int, album_name: str):
    """Добавляет фото в базу данных с привязкой к альбому"""
    cursor.execute("INSERT INTO photos (file_id, user_id, album_name) VALUES (?, ?, ?)", (file_id, user_id, album_name))
    conn.commit()

def get_random_photo_from_album(album_name: str):
    """Получает случайное фото из указанного альбома (от любого пользователя)"""
    cursor.execute("SELECT file_id FROM photos WHERE album_name = ?", (album_name,))
    photos = cursor.fetchall()

    if photos:
        return random.choice(photos)[0]  # Возвращаем случайное фото
    return None

def delete_album(album_name: str):
    """Удаляет все фото из указанного альбома"""
    cursor.execute("DELETE FROM photos WHERE album_name = ?", (album_name,))
    conn.commit()
