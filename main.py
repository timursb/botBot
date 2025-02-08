import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from database import add_photo, get_random_photo, clear_photos

# Токен
TOKEN = "7801520051:AAHRzF3Zj4U2dH6cxParfjeR0zf46lCfapM"

#  Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)  # Подключаем Router к Dispatcher

#  Логирование
logging.basicConfig(level=logging.INFO)

#  Создаём клавиатуру с кнопками
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📸 Добавить фото")],
        [KeyboardButton(text="🎲 Случайное фото")],
        [KeyboardButton(text="🛑 Завершить работу")]
    ],
    resize_keyboard=True
)

#  Команда /start
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я готов к работе. Используй кнопки ниже:", reply_markup=menu_keyboard)

#  Кнопка "Добавить фото"
@router.message(F.text == "📸 Добавить фото")
async def ask_for_photo(message: Message):
    await message.answer("Отправь мне фото, и оно будет сохранено в базе!")

#  Обработчик фотографий (сохраняем фото в базу)
@router.message(F.photo)
async def save_photo(message: Message):
    file_id = message.photo[-1].file_id
    add_photo(file_id)
    await message.answer("Фото сохранено! Теперь оно участвует в случайной выдаче. 📸")

#  Кнопка "Случайное фото"
@router.message(F.text == "🎲 Случайное фото")
async def send_random_photo(message: Message):
    file_id = get_random_photo()
    if file_id:
        await message.answer_photo(file_id, caption="Вот случайное фото из базы! 🎲")
    else:
        await message.answer("В базе пока нет фотографий. Отправь фото, чтобы добавить его!")

#  Кнопка "Завершить работу" (очищаем базу)
@router.message(F.text == "🛑 Завершить работу")
async def stop_bot(message: Message):
    clear_photos()
    logging.info("📁 Все фотографии удалены из базы!")  # Проверяем в логах

    # Проверяем, удалились ли фото
    if get_random_photo() is None:
        await message.answer("✅ Все фото удалены. Бот завершает работу. 🛑")
    else:
        await message.answer("⚠️ Ошибка! Фото почему-то не удалились. Проверь базу данных!")

#  Запуск бота
async def main():
    logging.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем зависшие обновления
    await dp.start_polling(bot)  # Запускаем бота

if __name__ == "__main__":
    asyncio.run(main())  # Запускаем асинхронный цикл
