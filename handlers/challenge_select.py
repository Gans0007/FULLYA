from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from db.db import database
from handlers.achievements import check_and_grant
from services.habits.habit_service import save_habit
from repositories.habits.habit_repo import get_habits_by_user, habit_exists, count_user_habits
from handlers.texts.challenge_select_texts import CHALLENGE_LEVELS, CHALLENGES, CHALLENGE_TEXTS

import logging
logger = logging.getLogger(__name__)

router = Router()

async def get_lang(user_id: int) -> str:
    row = await database.fetch_one("SELECT language FROM users WHERE user_id = :uid", {"uid": user_id})
    return row["language"] if row and row["language"] in CHALLENGE_TEXTS else "ru"

# ==== Клавиатуры ====
async def build_challenges_keyboard(level_key: str, user_id: int):
    lang = await get_lang(user_id)
    texts = CHALLENGE_TEXTS[lang]
    items = CHALLENGES.get(level_key, [])

    kb = InlineKeyboardMarkup(inline_keyboard=[], row_width=1)
    active_habits = await get_habits_by_user(user_id)
    active_ids = {h.challenge_id for h in active_habits if h.is_challenge and h.challenge_id is not None}

    completed_rows = await database.fetch_all(
        "SELECT challenge_id FROM completed_challenges WHERE user_id = :uid",
        {"uid": user_id}
    )
    completed_ids = {row["challenge_id"] for row in completed_rows}

    for idx, challenge in enumerate(items):
        challenge_id = challenge["id"]
        title = challenge[lang][0]
        days = challenge["days"]
        suffix = ""
        if challenge_id in active_ids:
            suffix = " 🔥"
        elif challenge_id in completed_ids:
            suffix = " ✅"
        btn = InlineKeyboardButton(
            text=f"{title} ({days} дн.){suffix}",
            callback_data=f"select_challenge:{level_key}:{idx}"
        )
        kb.inline_keyboard.append([btn])

    kb.inline_keyboard.append([
        InlineKeyboardButton(text=texts["back"], callback_data="take_challenge")
    ])
    return kb

# ==== Обработчики ====
@router.callback_query(lambda c: c.data == "take_challenge")
async def show_levels_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    texts = CHALLENGE_TEXTS[lang]
    levels = CHALLENGE_LEVELS[lang]

    logger.info(f"[{user_id}] 📖 Открыл меню уровней челленджей")

    kb = InlineKeyboardMarkup(inline_keyboard=[], row_width=1)
    for level_key, level_name in levels.items():
        kb.inline_keyboard.append([
            InlineKeyboardButton(text=level_name, callback_data=f"select_level:{level_key}")
        ])
    kb.inline_keyboard.append([
        InlineKeyboardButton(text=texts["back_to_menu"], callback_data="back_to_habit_menu")
    ])
    await callback.message.edit_text(texts["select_prompt"], reply_markup=kb)



@router.callback_query(lambda c: c.data.startswith("select_level:"))
async def show_challenges(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    texts = CHALLENGE_TEXTS[lang]

    _, level_key = callback.data.split(":")
    level_name = CHALLENGE_LEVELS[lang].get(level_key, "?")

    logger.info(f"[{user_id}] 📚 Открыл список челленджей уровня {level_key} - {level_name}")

    await callback.message.edit_text(
        texts["challenges_of_level"].format(level=level_name),
        reply_markup=await build_challenges_keyboard(level_key, user_id)
    )



@router.callback_query(lambda c: c.data.startswith("select_challenge:"))
async def confirm_challenge(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    texts = CHALLENGE_TEXTS[lang]

    _, level_key, idx_str = callback.data.split(":")
    idx = int(idx_str)
    challenge = CHALLENGES[level_key][idx]
    title, desc = challenge[lang]
    days = challenge["days"]

    logger.info(f"[{user_id}] 🧐 Просмотр челленджа: {title} ({days} дн.), уровень {level_key}")

    if level_key == "level_0":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=texts["viewed_button"], callback_data=f"viewed_only:{level_key}:{idx}")],
            [InlineKeyboardButton(text=texts["back"], callback_data=f"select_level:{level_key}")]
        ])
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=texts["take_challenge"], callback_data=f"add_challenge:{level_key}:{idx}")],
            [InlineKeyboardButton(text=texts["back"], callback_data=f"select_level:{level_key}")]
        ])

    await callback.message.edit_text(
        texts["confirm_challenge"].format(title=title, days=days, desc=desc),
        parse_mode="HTML",
        reply_markup=kb
    )



@router.callback_query(lambda c: c.data.startswith("add_challenge:"))
async def add_challenge(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    texts = CHALLENGE_TEXTS[lang]

    if await count_user_habits(user_id) >= 10:
        logger.info(f"[{user_id}] ❌ Превышен лимит активных привычек при добавлении челленджа")
        await callback.message.answer(texts["too_many_active"])
        return

    _, level_key, idx_str = callback.data.split(":")
    idx = int(idx_str)
    challenge = CHALLENGES[level_key][idx]
    challenge_id = challenge["id"]
    title, desc = challenge[lang]
    days = challenge["days"]
    ctype = challenge["type"]

    if await habit_exists(user_id, title):
        logger.info(f"[{user_id}] ⚠️ Попытка повторно взять активный челлендж: {title}")
        await callback.message.answer(texts["already_active"])
        return

    await save_habit(
        user_id=user_id,
        name=title,
        days=days,
        description=desc,
        is_challenge=True,
        confirm_type=ctype,
        challenge_id=challenge_id
    )

    total_challenges = await database.fetch_val(
        "SELECT COUNT(*) FROM habits WHERE user_id = :uid AND is_challenge = TRUE",
        {"uid": user_id}
    )
    await check_and_grant(user_id, "challenge_create", total_challenges, callback.bot)

    logger.info(f"[{user_id}] ✅ Добавил челлендж: {title} ({days} дн.)")
    await callback.message.edit_text(texts["added_success"])



@router.callback_query(lambda c: c.data.startswith("viewed_only:"))
async def handle_viewed_only(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    texts = CHALLENGE_TEXTS[lang]

    _, level_key, idx_str = callback.data.split(":")
    idx = int(idx_str)
    challenge = CHALLENGES[level_key][idx]
    challenge_id = challenge["id"]
    title, _ = challenge[lang]

    exists = await database.fetch_val(
        "SELECT COUNT(*) FROM completed_challenges WHERE user_id = :uid AND challenge_id = :cid",
        {"uid": user_id, "cid": challenge_id}
    )
    if exists:
        logger.info(f"[{user_id}] 📌 Уже ранее просмотрел челлендж: {title}")
        await callback.answer(texts["already_viewed"])
        return

    await database.execute(
        "INSERT INTO completed_challenges (user_id, challenge_id) VALUES (:uid, :cid)",
        {"uid": user_id, "cid": challenge_id}
    )
    await database.execute(
        "UPDATE users SET xp_balance = xp_balance + 1 WHERE user_id = :uid",
        {"uid": user_id}
    )
    await check_and_grant(user_id, "challenge_done", 1, callback.bot)

    logger.info(f"[{user_id}] 👁 Отметил челлендж как просмотренный: {title}")
    await callback.message.edit_text(texts["viewed_success"].format(title=title))



@router.callback_query(lambda c: c.data == "back_to_habit_menu")
async def back_to_habit_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    texts = CHALLENGE_TEXTS[lang]

    total = await count_user_habits(user_id)
    logger.info(f"[{user_id}] ↩️ Вернулся в меню привычек ({total}/10)")

    text = texts["habit_info"].format(total=total)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts["add_habit"], callback_data="add_habit_custom")],
        [InlineKeyboardButton(text=texts["take_from_list"], callback_data="take_challenge")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
