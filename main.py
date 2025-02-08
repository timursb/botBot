import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from database import add_photo, get_random_photo

#  Токен бота
TOKEN = "7918646403:AAGWfUIq5xPzOwwyfQG2eAu3bYwiWVPxOK0"

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Логирование
logging.basicConfig(level=logging.INFO)

#  Обработчик фотографий
@dp.message(lambda message: message.photo)
async def save_photo(message: Message):
    file_id = message.photo[-1].file_id  # Получаем ID самого большого фото
    add_photo(file_id)  # Сохраняем в базу
    await message.answer("Фото сохранено! Теперь оно участвует в рандоме. 📸")

#  Отправка случайной фотографии
@dp.message(Command("random"))
async def send_random_photo(message: Message):
    file_id = get_random_photo()
    if file_id:
        await bot.send_photo(message.chat.id, file_id, caption="Вот случайное фото из базы! 🎲")
    else:
        await message.answer("В базе пока нет фотографий. Отправь фото, чтобы добавить его!")

#  Стартовое сообщение
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Отправь мне фото, и оно будет участвовать в случайной выдаче. Используй /random, чтобы получить случайное фото!")

#  Функция запуска бота
async def main():
    logging.info("Бот запускается...")
    await dp.start_polling(bot)
    logging.info("Бот завершил работу.")  # Этот код никогда не выполнится, пока бот работает

if __name__ == "__main__":
    logging.info("Запуск бота...")
    asyncio.run(main())
