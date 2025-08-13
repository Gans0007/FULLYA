# handlers/honor_handler.py

import logging
from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.db import database
from utils.streak_emojis import get_streak_emoji
# from services.profile.profile_service import get_liga_by_xp  # ⛔️ больше не нужно
from utils.ui import safe_replace_message
from handlers.texts.honor_board_texts import HONOR_BOARD_TEXTS, HONOR_BOARD_BUTTONS
from handlers.texts.achievements_texts import LIGAS  # ✅ добавили

router = Router()
logger = logging.getLogger(__name__)

# ---------- helpers (язык, имя) ----------
async def get_lang(user_id: int) -> str:
    row = await database.fetch_one("SELECT language FROM users WHERE user_id = :uid", {"uid": user_id})
    return row["language"] if row and row["language"] in HONOR_BOARD_TEXTS else "ru"

async def get_display_name(bot, uid: int, username: str) -> str:
    if username:
        return f"@{username}"
    try:
        chat = await bot.get_chat(uid)
        return chat.full_name
    except Exception:
        return f"ID:{uid}"

async def build_honor_keyboard(lang: str):
    b = HONOR_BOARD_BUTTONS[lang]
    kb = InlineKeyboardBuilder()
    kb.button(text=b["world"], callback_data="honor_world")
    kb.button(text=b["league"], callback_data="honor_league")
    kb.button(text=b["back"], callback_data="back_to_about")
    kb.adjust(2, 1)
    return kb.as_markup()

# ---------- NEW: league helpers (ID + локализация) ----------
def get_league_id_by_xp(xp: int) -> int:
    """
    Возвращает ID лиги (1..N) по интервалам XP.
    Интервалы одинаковые во всех языках, берём ru как эталон.
    """
    for idx, (xmin, xmax, _name, _emoji, _quote) in enumerate(LIGAS["ru"], start=1):
        if xmin <= xp <= xmax:
            return idx
    return len(LIGAS["ru"])

def get_league_name_emoji(lang: str, league_id: int) -> tuple[str, str]:
    """
    Возвращает локализованные (name, emoji) по языку и league_id.
    """
    lang = lang if lang in LIGAS else "ru"
    # защита от выхода за границы
    league_id = max(1, min(league_id, len(LIGAS[lang])))
    _xmin, _xmax, name, emoji, _quote = LIGAS[lang][league_id - 1]
    return name, emoji

# ---------- world top (без изменений) ----------
async def show_top10_async(msg_or_callback: types.Message | types.CallbackQuery):
    user_id = msg_or_callback.from_user.id
    lang = await get_lang(user_id)
    t = HONOR_BOARD_TEXTS[lang]
    b = HONOR_BOARD_BUTTONS[lang]

    logger.info(f"[HONOR] Пользователь {user_id} запросил ТОП 10")

    total_users = await database.fetch_val("SELECT COUNT(*) FROM users")

    rows = await database.fetch_all("""
        SELECT u.user_id, COALESCE(p.username, '') AS username,
               u.xp_balance, u.active_days, u.current_streak
        FROM users u
        LEFT JOIN profiles p ON u.user_id = p.user_id
        ORDER BY u.xp_balance DESC
        LIMIT 10
    """)

    medals = ["🥇", "🥈", "🥉"] + [f"{i}." for i in range(4, 11)]

    table_lines = [t["title"], t["total_users"].format(count=total_users), "<pre>"]
    table_lines.append(f"{'№':<3}{'Ник':<15}{'XP':>6}{'Дни':>6}{'🔥':>4}")
    table_lines.append(t["table_divider"])

    for i, row in enumerate(rows):
        uid, username, xp, days, streak = row.values()
        display_nick = (await get_display_name(msg_or_callback.bot, uid, username))[:13]
        medal = medals[i] if i < len(medals) else f"{i+1}."
        table_lines.append(f"{medal:<3}{display_nick:<13}{xp:>6}{days:>6}{streak:>6}")

    if not any(row["user_id"] == user_id for row in rows):
        table_lines.append(t["not_in_top"])
        user_place_row = await database.fetch_one("""
            SELECT r, xp_balance, active_days, current_streak FROM (
                SELECT user_id, xp_balance, active_days, current_streak,
                       ROW_NUMBER() OVER (ORDER BY xp_balance DESC) AS r
                FROM users
            ) sub WHERE user_id = :uid
        """, {"uid": user_id})

        username = await database.fetch_val("SELECT username FROM profiles WHERE user_id = :uid", {"uid": user_id}) or ""

        if user_place_row:
            rank = user_place_row["r"]
            xp = user_place_row["xp_balance"]
            days = user_place_row["active_days"]
            streak = user_place_row["current_streak"]
            display_nick = (await get_display_name(msg_or_callback.bot, user_id, username))[:13]
            table_lines.append(f"{rank}. {display_nick:<13}{xp:>6}{days:>6}{streak:>6}")

    table_lines.append("</pre>")
    final_text = "\n".join(table_lines)

    reply_markup = await build_honor_keyboard(lang)

    if isinstance(msg_or_callback, types.Message):
        await msg_or_callback.answer(final_text, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await safe_replace_message(msg_or_callback.message, final_text, reply_markup=reply_markup, parse_mode="HTML")
        await msg_or_callback.answer()

# ---------- league top (исправлено на ID) ----------
@router.callback_query(F.data == "honor_league")
async def handle_honor_league(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = HONOR_BOARD_TEXTS[lang]

    logger.info(f"[HONOR] Пользователь {user_id} запросил ТОП 10 по лиге")

    user_row = await database.fetch_one("SELECT xp_balance FROM users WHERE user_id = :uid", {"uid": user_id})
    if not user_row:
        await callback.answer(t["not_ranked"], show_alert=True)
        return

    user_xp = user_row["xp_balance"]
    user_league_id = get_league_id_by_xp(user_xp)
    league_name, league_emoji = get_league_name_emoji(lang, user_league_id)

    rows_all = await database.fetch_all("""
        SELECT u.user_id, COALESCE(p.username, '') AS username,
               u.xp_balance, u.active_days, u.current_streak
        FROM users u
        LEFT JOIN profiles p ON u.user_id = p.user_id
        ORDER BY u.xp_balance DESC
    """)

    # фильтруем по league_id, а не по названию
    same_league = []
    for r in rows_all:
        r_league_id = get_league_id_by_xp(r["xp_balance"])
        if r_league_id == user_league_id:
            same_league.append(r)

    top10 = same_league[:10]

    table_lines = [
        t["league_title"].format(league=league_name, emoji=league_emoji),
        t["league_total"].format(count=len(same_league)),
        "<pre>",
        f"{'№':<3}{'Ник':<12}{'XP':>5}{'Дни':>5}{'🔥':>4}",
        t["league_table_divider"]
    ]

    medals = ["🥇", "🥈", "🥉"] + [f"{i}." for i in range(4, 11)]

    for i, row in enumerate(top10):
        uid, username, xp, days, streak = row.values()
        display_nick = (await get_display_name(callback.bot, uid, username))[:12]
        table_lines.append(f"{medals[i]:<3}{display_nick:<12}{xp:>5}{days:>5}{streak:>4}")

    if not any(row["user_id"] == user_id for row in top10):
        table_lines.append(t["league_table_divider"])
        for idx, row in enumerate(same_league, start=1):
            if row["user_id"] == user_id:
                username = row["username"]
                xp = row["xp_balance"]
                days = row["active_days"]
                streak = row["current_streak"]
                display_nick = (await get_display_name(callback.bot, user_id, username))[:12]
                table_lines.append(f"{idx}. {display_nick:<12}{xp:>5}{days:>5}{streak:>4}")
                break

    table_lines.append("</pre>")
    reply_markup = await build_honor_keyboard(lang)

    await safe_replace_message(callback.message, "\n".join(table_lines), reply_markup=reply_markup, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "honor_world")
async def handle_honor_world(callback: CallbackQuery):
    await show_top10_async(callback)
