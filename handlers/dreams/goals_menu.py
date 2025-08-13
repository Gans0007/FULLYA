import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from handlers.subscription_guard import has_active_subscription
from handlers.texts.menu_texts import MAIN_MENU_TEXTS
from handlers.texts.dreams_texts import DREAMS_MENU_TEXT, DREAMS_MENU_BUTTONS
from db.db import database

logger = logging.getLogger(__name__)
router = Router()


def _txt_lang(lang: str) -> str:
    """Map DB lang -> texts lang keys (DREAMS_MENU_TEXT uses 'ua' instead of 'uk')."""
    return "ua" if lang == "uk" else lang


async def get_lang(user_id: int) -> str:
    """Safely fetch user's language (fallback to 'ru')."""
    row = await database.fetch_one(
        """
        SELECT COALESCE(language, 'ru') AS language
        FROM users
        WHERE user_id = :uid
        """,
        {"uid": user_id},
    )
    lang = row["language"] if row else "ru"
    # validate against buttons dict since it's superset ('uk' exists there)
    return lang if lang in DREAMS_MENU_BUTTONS else "ru"


def build_goals_main_menu(lang: str) -> InlineKeyboardMarkup:
    t = DREAMS_MENU_BUTTONS.get(lang, DREAMS_MENU_BUTTONS["ru"])
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["goals"],  callback_data="view_goals")],
            [InlineKeyboardButton(text=t["plans"],  callback_data="view_plans")],
            [InlineKeyboardButton(text=t["dreams"], callback_data="view_dreams")],
            [InlineKeyboardButton(text=t["hall"],   callback_data="hall_of_fame")],
            [InlineKeyboardButton(text=t["add"],    callback_data="add_new")],
        ]
    )


async def _send_goals_menu(message: Message, lang: str) -> None:
    await message.answer(
        DREAMS_MENU_TEXT[_txt_lang(lang)],
        reply_markup=build_goals_main_menu(lang),
    )


# === Entry from main app keyboard ("Dreams/Plans" button) ===
@router.message(lambda msg: msg.text in [t["dreams"] for t in MAIN_MENU_TEXTS.values()])
async def handle_goals_menu(message: Message):
    user_id = message.from_user.id
    if not await has_active_subscription(user_id, message):
        return

    lang = await get_lang(user_id)
    logger.info(f"[DREAMS MENU] Пользователь {user_id} открыл раздел мечт/планов")
    await _send_goals_menu(message, lang)


# === Return/back from inside this section (inline button callback) ===
@router.callback_query(F.data == "goals_menu")
async def handle_goals_menu_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not await has_active_subscription(user_id, callback.message):
        await callback.answer()
        return

    lang = await get_lang(user_id)
    logger.info(f"[DREAMS MENU] Пользователь {user_id} вернулся в главное меню раздела")
    await callback.message.answer(
        DREAMS_MENU_TEXT[_txt_lang(lang)],
        reply_markup=build_goals_main_menu(lang),
    )
    await callback.answer()