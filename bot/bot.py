import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from database import add_photo, get_random_photo_from_album, delete_album

# Токен бота
TOKEN = "7801520051:AAHRzF3Zj4U2dH6cxParfjeR0zf46lCfapM"

# Создаём бота и диспетчер
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)
# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаём клавиатуру
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📸 Добавить фото")],
        [KeyboardButton(text="📂Случайное фото из альбома")],
        [KeyboardButton(text="🗑 Удалить альбом")],
        [KeyboardButton(text="🛑 Завершить работу")]
    ],
    resize_keyboard=True
)

# FSM-состояния
class PhotoState(StatesGroup):
    waiting_for_album_name = State()
    waiting_for_photos = State()

class AlbumState(StatesGroup):
    waiting_for_album_request = State()
    waiting_for_album_deletion = State()  # Состояние для удаления альбома

# Команда /start
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Отправь фото, и я его сохраню!", reply_markup=menu_keyboard)

# Кнопка "Добавить фото"
@router.message(F.text == "📸 Добавить фото")
async def ask_for_album_name(message: Message, state: FSMContext):
    await message.answer("Введите название альбома, в который хотите добавить фото:")
    await state.set_state(PhotoState.waiting_for_album_name)

# Получение названия альбома
@router.message(PhotoState.waiting_for_album_name)
async def receive_album_name(message: Message, state: FSMContext):
    album_name = message.text
    await state.update_data(album_name=album_name)
    await message.answer(f"Отлично! Теперь отправьте фото для альбома {album_name}. Можно сразу несколько!")
    await state.set_state(PhotoState.waiting_for_photos)

# Обработка нескольких фото
@router.message(PhotoState.waiting_for_photos, F.photo)
async def save_photos(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    album_name = data.get("album_name")
    for photo in message.photo:
        add_photo(photo.file_id, user_id, album_name)

    await message.answer(f"Фото добавлены в альбом {album_name}! 📸")
    await state.clear()

# Кнопка "Случайное фото из альбома"
@router.message(F.text == "📂Случайное фото из альбома")
async def ask_for_album_name_for_request(message: Message, state: FSMContext):
    await message.answer("Введите название альбома, из которого хотите получить фото:")
    await state.set_state(AlbumState.waiting_for_album_request)

# Получение случайного фото из альбома
@router.message(AlbumState.waiting_for_album_request)
async def send_photo_from_album(message: Message, state: FSMContext):
    album_name = message.text
    user_id = message.from_user.id

    file_id = get_random_photo_from_album(user_id, album_name)

    if file_id:
        await message.answer_photo(file_id, caption=f"Вот случайное фото из альбома {album_name}! 📂")
        await state.update_data(last_album=album_name)
    else:
        await message.answer(f"В альбоме {album_name} пока нет фото или он не существует.")

    await state.clear()

# Кнопка "Удалить альбом" (запрос названия альбома)
@router.message(F.text == "🗑 Удалить альбом")
async def ask_for_album_deletion(message: Message, state: FSMContext):
    await message.answer("Введите название альбома, который хотите удалить:")
    await state.set_state(AlbumState.waiting_for_album_deletion)

# Удаление альбома после ввода пользователем названия
@router.message(AlbumState.waiting_for_album_deletion)
async def delete_album_photos(message: Message, state: FSMContext):
    album_name = message.text
    delete_album(album_name)  # Удаляем альбом
    await message.answer(f"Все фото из альбома {album_name} удалены. 🗑")
    await state.clear()

# Кнопка "Завершить работу"
@router.message(F.text == "🛑 Завершить работу")
async def stop_bot(message: Message):
    await message.answer("Бот завершает работу. Чтобы запустить его снова, используйте /start")

# Запуск бота
async def main():
    logging.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import sys

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
