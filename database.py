import sqlite3

DB_PATH = "database.db"

#  Добавление фото в базу
def add_photo(file_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS photos (file_id TEXT)")
    cursor.execute("INSERT INTO photos (file_id) VALUES (?)", (file_id,))
    conn.commit()
    conn.close()

#  Получение случайного фото
def get_random_photo():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM photos ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

#  Очистка базы данных (удаляем все фото)
def clear_photos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM photos")  # Удаляем фото
    conn.commit()
    conn.close()
    print("📁 База данных очищена!")  # Проверка в консоли
