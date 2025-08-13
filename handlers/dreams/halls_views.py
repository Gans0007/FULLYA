from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils.ui import safe_replace_message
from db.db import database
from handlers.texts.dreams_texts import HALLS_TEXTS
import logging

logger = logging.getLogger(__name__)
router = Router()

async def get_lang(user_id: int) -> str:
    row = await database.fetch_one("SELECT language FROM users WHERE user_id = :uid", {"uid": user_id})
    return row["language"] if row and row["language"] in HALLS_TEXTS else "ru"

@router.callback_query(F.data == "hall_of_fame")
async def view_hall_of_fame(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = HALLS_TEXTS[lang]

    logger.info(f"[HALL] Пользователь {user_id} открыл Зал Славы")

    completed_goals = await database.fetch_all(
        "SELECT text, created_at, done_at FROM goals WHERE user_id = :uid AND is_done = true",
        {"uid": user_id}
    )
    completed_dreams = await database.fetch_all(
        "SELECT text, created_at, done_at FROM dreams WHERE user_id = :uid AND is_done = true",
        {"uid": user_id}
    )

    if not completed_goals and not completed_dreams:
        logger.info(f"[HALL] У пользователя {user_id} нет завершенных целей и мечт")
        await callback.answer(t["empty"])
        return

    text = t["title"]

    if completed_goals:
        text += t["completed_goals_title"]
        for row in completed_goals:
            date_from = row["created_at"].strftime("%d.%m.%Y") if row["created_at"] else "?"
            date_to = row["done_at"].strftime("%d.%m.%Y") if row["done_at"] else "?"
            text += t["goal_line"].format(text=row["text"], from_date=date_from, to_date=date_to)

    if completed_dreams:
        text += t["completed_dreams_title"]
        for row in completed_dreams:
            date_from = row["created_at"].strftime("%d.%m.%Y") if row["created_at"] else "?"
            date_to = row["done_at"].strftime("%d.%m.%Y") if row["done_at"] else "?"
            text += t["dream_line"].format(text=row["text"], from_date=date_from, to_date=date_to)

    await callback.message.answer(text, parse_mode="HTML")

@router.callback_query(F.data == "back_to_dreams_plans_menu")
async def back_to_dreams_plans_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = HALLS_TEXTS[lang]

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["buttons"]["goals"], callback_data="view_goals")],
        [InlineKeyboardButton(text=t["buttons"]["plans"], callback_data="view_plans")],
        [InlineKeyboardButton(text=t["buttons"]["dreams"], callback_data="view_dreams")],
        [InlineKeyboardButton(text=t["buttons"]["hall"], callback_data="hall_of_fame")],
        [InlineKeyboardButton(text=t["buttons"]["add"], callback_data="add_new")]
    ])

    await callback.message.answer(
        t["back_menu_title"],
        reply_markup=markup,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("set_dream_done_"))
async def set_dream_done(callback: CallbackQuery):
    dream_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = HALLS_TEXTS[lang]

    await database.execute(
        """
        UPDATE dreams
        SET is_done = true, done_at = NOW()
        WHERE id = :id AND user_id = :uid
        """,
        {"id": dream_id, "uid": user_id}
    )

    logger.info(f"[HALL] Пользователь {user_id} отметил мечту {dream_id} как исполненную")

    await safe_replace_message(callback.message, t["dream_done"], parse_mode="HTML")
    await callback.answer()
