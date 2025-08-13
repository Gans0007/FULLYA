import logging
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.profile.profile_service import get_user_profile_summary
from handlers.about_me.about_menu import get_about_inline_menu
from repositories.profiles.profile_repository import (
    get_profile,
    update_profile_field,
)
from handlers.about_me.members import show_participants
from utils.ui import safe_replace_message

# ⬇️ достаём язык пользователя
from db.db import database
from handlers.texts.about_me import PROFILE_TEXTS

logger = logging.getLogger(__name__)
router = Router()


async def get_lang(user_id: int) -> str:
    """Возвращает язык интерфейса пользователя с fallback на 'ru'."""
    row = await database.fetch_one(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id},
    )
    default = "ru"
    if not row:
        return default
    try:
        value = row["language"]  # Record поддерживает индексацию, но не .get()
    except Exception:
        return default
    return value if value in PROFILE_TEXTS else default


@router.callback_query(F.data == "about_profile")
async def show_profile(callback: types.CallbackQuery):
    """Показывает профиль пользователя (все тексты мультиязычные)."""
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    T = PROFILE_TEXTS[lang]

    profile = await get_profile(user_id)
    logger.info(f"[PROFILE] Открыт просмотр профиля пользователя {user_id}")

    if profile:
        visibility_text = (
            T["visibility_open"]
            if profile.get("is_visible", True)
            else T["visibility_closed"]
        )
        username = f"@{profile['username']}" if profile.get("username") else "—"
        text = (
            f"{visibility_text}\n\n"
            f"{T['label_name']}: {profile.get('name', '—')}\n"
            f"{T['label_username']}: {username}\n"
            f"{T['label_age']}: {profile.get('age', '—')}\n"
            f"{T['label_spec']}: {profile.get('specialization', '—')}\n"
            f"{T['label_help']}: {profile.get('help_text', '—')}\n"
            f"{T['label_message']}: {profile.get('message', '—')}"
        )
    else:
        text = T["profile_empty"]
        logger.info(f"[PROFILE] У пользователя {user_id} пока нет заполненного профиля")

    builder = InlineKeyboardBuilder()
    if profile:
        builder.button(
            text=T["btn_open"] if profile.get("is_visible", True) else T["btn_closed"],
            callback_data="toggle_visibility",
        )
    builder.button(text=T["btn_edit"], callback_data="edit_profile")
    builder.button(text=T["btn_back"], callback_data="back_to_about")
    builder.adjust(2 if profile else 1)

    await safe_replace_message(
        callback.message,
        text=text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "back_to_about")
async def back_to_about(callback: types.CallbackQuery):
    """Возврат в меню 'Обо мне' (мультиязычная шапка)."""
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    T = PROFILE_TEXTS[lang]

    logger.info(
        f"[PROFILE] Пользователь {user_id} вернулся в главное меню 'Обо мне'"
    )

    usdt, xp, liga, quote = await get_user_profile_summary(user_id)
    markup = await get_about_inline_menu(user_id)

    text = T["about_header"].format(usdt=usdt, xp=xp, liga=liga, quote=quote)
    await callback.message.answer(text, reply_markup=markup, parse_mode="HTML")


@router.callback_query(F.data == "toggle_visibility")
async def toggle_visibility(callback: types.CallbackQuery):
    """Переключение видимости профиля."""
    user_id = callback.from_user.id
    profile = await get_profile(user_id)
    if not profile:
        logger.warning(
            f"[PROFILE] Не найден профиль пользователя {user_id} при переключении видимости"
        )
        await callback.answer()
        return

    new_visibility = not bool(profile.get("is_visible", True))
    await update_profile_field(
        user_id, "is_visible", new_visibility, callback.from_user.username or ""
    )
    logger.info(
        f"[PROFILE] Пользователь {user_id} переключил видимость на "
        f"{'Открытый' if new_visibility else 'Скрытый'}"
    )

    # Перерисовываем экран профиля тем же методом
    await show_profile(callback)
    await callback.answer()


@router.callback_query(F.data == "about_participants")
async def show_participants_from_about(callback: types.CallbackQuery):
    """Показывает список участников через раздел 'Обо мне'"""
    await show_participants(callback, replace=False)
