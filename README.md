📸 RandomchikPhoto_bot

##Описание

**Randomchik Photo Bot** — это телеграм-бот, разработанный с использованием Aiogram, который позволяет пользователям:

✅ Добавлять фотографии в альбомы.
✅ Получать случайное фото из конкретного альбома.
✅ Удалять альбомы вместе со всеми фотографиями.
✅ Завершать работу.

**Бот хранит фотографии в базе данных SQLite и работает в режиме polling.**

#🚀 Функционал

**Основные команды:**

**/start** — Запуск бота и отображение меню.
**📸 Добавить фото**— Добавление фото в указанный альбом.
**📂 Случайное фото из альбома** — Получение случайного фото из конкретного альбома.
**🗑 Удалить альбом** — Удаление альбома и всех его фотографий.
**🛑 Завершить работу** — Остановка работы бота.

#📦 Установка и настройка

**1️⃣ Клонирование репозитория**

https://github.com/timursb/botBot

**2️⃣ Установка зависимостей**

Создайте виртуальное окружение (рекомендуется) и установите зависимости:
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt

**3️⃣ Создание и настройка базы данных**

Перед первым запуском убедитесь, что в корне проекта находится база photos.db. Если её нет, бот создаст её автоматически.

**4️⃣ Указание токена бота**

Создайте файл .env и добавьте в него токен вашего бота(можно получить в телеграмм боте @BotFather)
TOKEN=ТВОЙ_ТОКЕН_БОТА

#📜 Структура проекта

Randomchik-Photo-bot/
│── database.py            # Работа с базой данных SQLite
│── main.py                # Основной файл бота
│── requirements.txt       # Список зависимостей
│── README.md              # Описание проекта
│── photos.db              # База данных (создается автоматически)

#🔧 Используемые технологии
**Python 3.10+**
**Aiogram 3.0**
**SQLite**
**Asyncio**

#🚀 Запуск бота

**python main.py**

#🎯 Пример работы

**Добавление фото:**
1. Бот запрашивает название альбома.
2. Затем позволяет отправлять фотографии.
**Получение случайного фото:**
1. Пользователь вводит название альбома.
2. Бот отправляет случайное фото из этого альбома.
**Удаление альбома:**
1. Пользователь вводит название альбома.
2. Бот удаляет альбом и все его фото.

**👍 Удачного пользования!🎉**
