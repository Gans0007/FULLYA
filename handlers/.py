from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import ADMIN_ID
from keyboards.monetization import get_main_monetization_menu
from db.db import database  # добавлено для запроса к БД
import logging


router = Router()


@router.message(F.text == "📥 Полная версия")
async def handle_full_version(message: types.Message):
    import logging
    logging.getLogger(__name__).info(
        f"[DEBUG] Кнопка 'Полная версия' нажата. text={repr(message.text)}, user_id={message.from_user.id}"
    )

    # Получаем XP пользователя
    query = "SELECT xp_balance FROM users WHERE user_id = :user_id"
    row = await database.fetch_one(query, {"user_id": message.from_user.id})
    xp = row[0] if row else 0

    # Текст с эмодзи и подстановкой xp
    text = (
        "🔓 <b>YOUR AMBITIONS — больше, чем бот</b>\n"
        "Это <b>твоя социальная сеть</b>, если ты:\n\n"
        "•  Хочешь выработать <b>стальные привычки</b>\n"
        "•  Ищешь <b>единомышленников и сильное окружение</b>\n"
        "•  Чётко видишь цель, но чувствуешь, что для рывка чего‑то не хватает\n\n"
        "⚡ <b>СЕЙЧАС ТВОЙ ШАНС</b>\n"
        "С 60 хр — <b>скидка 30%</b> на полную версию!\n"
        f"У тебя сейчас — <b>{xp} хр</b>.\n\n"
        "Что даёт <b>полная версия?</b>\n"
        "🚀 <b>Безлимит</b> на привычки и челленджи\n"
        "💸 <b>Ежемесячные выплаты</b> за рефералов\n"
        "🏆 <b>Топ‑10 лучших</b> в мире или среди друзей\n"
        "🔒 <b>Закрытый чат VIP‑участников</b>\n"
        "👤 <b>Профили участников</b> — смотри, кто рядом с тобой\n"
        "📅 Личные <b>заметки, мечты, цели, планы</b> с напоминаниями\n"
        "📊 <b>Подробная статистика и прогресс</b>\n"
        "🥇 <b>Лиги, уровни, достижения</b>\n"
        "🎁 <b>Физические награды</b> от команды <b>Your Ambitions</b>\n\n"
        "Тебе не нужны чудеса.\n"
        "Тебе нужен <b>прогресс</b>.\n\n"
        "<b>Ты в игре? 🔥</b>"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Приобрести полный доступ", callback_data="full_access_coming_soon")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="monetization_back")]
    ])

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "full_access_coming_soon")
async def handle_full_access_coming_soon(callback: CallbackQuery):
    await callback.answer("⏳ Скоро будет доступно!", show_alert=True)

@router.message(F.photo)
async def handle_photo(message: types.Message):
    # Берем самое большое по качеству фото
    photo = message.photo[-1]
    file_id = photo.file_id

    logging.getLogger(__name__).info(f"[PHOTO] file_id={file_id} from user_id={message.from_user.id}")
    print(f"[PHOTO] file_id={file_id} from user_id={message.from_user.id}")  # для вывода прямо в консоль

    await message.answer(f"ID этой фотографии:\n<code>{file_id}</code>", parse_mode="HTML")