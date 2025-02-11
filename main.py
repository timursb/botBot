import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from database import add_photo, get_random_photo, clear_photos

# Токен бота
TOKEN = "7801520051:AAHRzF3Zj4U2dH6cxParfjeR0zf46lCfapM"

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаём клавиатуру
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📸 Добавить фото")],
        [KeyboardButton(text="🎲 Случайное фото")],
        [KeyboardButton(text="🛑 Завершить работу")]
    ],
    resize_keyboard=True
)


# Команда /start
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Отправь фото, и я его сохраню!", reply_markup=menu_keyboard)


# Кнопка "Добавить фото"
@router.message(F.text == "📸 Добавить фото")
async def ask_for_photo(message: Message):
    await message.answer("Отправь мне фото, и оно будет сохранено!")


# Обработка фотографий (сохраняем с user_id)
@router.message(F.photo)
async def save_photo(message: Message):
    file_id = message.photo[-1].file_id
    user_id = message.from_user.id  # Получаем user_id
    add_photo(file_id, user_id)
    await message.answer("Фото сохранено! Теперь оно участвует в случайной выдаче. 📸")


# Кнопка "Случайное фото"
@router.message(F.text == "🎲 Случайное фото")
async def send_random_photo(message: Message):
    user_id = message.from_user.id
    file_id = get_random_photo(user_id)

    if file_id:
        await message.answer_photo(file_id, caption="Вот случайное фото из твоих сохранённых! 🎲")
    else:
        await message.answer("У тебя пока нет загруженных фото. Добавь хотя бы одно!")


# Кнопка "Завершить работу" (очищает базу)
@router.message(F.text == "🛑 Завершить работу")
async def stop_bot(message: Message):
    clear_photos()
    await message.answer("✅ Все фото удалены. Бот завершает работу.")


# Запуск бота
async def main():
    logging.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


