from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.texts.about_me import ABOUT_MENU_TEXTS
from db.db import database


def _normalize_lang(lang: str) -> str:
    # Если где-то хранится "ua", а словари используют "uk" (или наоборот)
    if lang == "ua" and "uk" in ABOUT_MENU_TEXTS:
        return "uk"
    if lang == "uk" and "ua" in ABOUT_MENU_TEXTS:
        return "ua"
    return lang


async def get_user_language(user_id: int) -> str:
    row = await database.fetch_one(
        """
        SELECT COALESCE(language, 'ru') AS language
        FROM users
        WHERE user_id = :uid
        """,
        {"uid": user_id},
    )
    lang = _normalize_lang(row["language"] if row else "ru")
    return lang if lang in ABOUT_MENU_TEXTS else "ru"


async def get_about_inline_menu(user_id: int) -> InlineKeyboardMarkup:
    lang = await get_user_language(user_id)
    texts = ABOUT_MENU_TEXTS.get(lang, ABOUT_MENU_TEXTS["ru"])

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts["referrals"],   callback_data="about_referrals"),
                InlineKeyboardButton(text=texts["stats"],       callback_data="about_stats"),
            ],
            [
                InlineKeyboardButton(text=texts["profile"],     callback_data="about_profile"),
                InlineKeyboardButton(text=texts["participants"], callback_data="about_participants"),
            ],
            [
                InlineKeyboardButton(text=texts["settings"],    callback_data="about_options"),
            ],
        ]
    )
