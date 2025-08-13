# handlers/about_me/statistics.py
import logging
from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from db.db import database  # databases
from handlers.texts.achievements_texts import LIGAS
from utils.ui import safe_replace_message

# ⬇️ тексты берём из handlers.texts.about_me (как у тебя в других файлах)
from handlers.texts.about_me import ABOUT_MENU_TEXTS, STATISTICS_TEXTS

router = Router()
logger = logging.getLogger(__name__)

TOTAL_ACHIEVEMENTS = 99

# --- helpers -----------------------------------------------------------------

async def _get_lang(user_id: int) -> str:
    """Язык интерфейса пользователя с фолбэком на ru."""
    lang = await database.fetch_val(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id}
    )
    return (lang or "ru").lower()

def _stats_variants() -> set[str]:
    """Все варианты текста пункта меню 'Статистика' на разных языках."""
    return {v["stats"] for v in ABOUT_MENU_TEXTS.values()}

def _get_league_i18n(xp: int, lang: str) -> tuple[str, str, str, int]:
    """
    Возвращает (league_name, emoji, quote, next_level_xp_min) по LIGAS[lang].
    next_level_xp_min — минимальный XP следующей лиги (для расчёта 'xp_to_next').
    Для последней лиги возвращаем текущий xp, чтобы 'xp_to_next' был 0.
    """
    bundle = LIGAS.get(lang) or LIGAS["ru"]
    for i, (lo, hi, name, emoji, quote) in enumerate(bundle):
        if lo <= xp <= hi:
            # min XP следующей лиги, либо текущий XP, если это последняя
            next_min = bundle[i + 1][0] if i + 1 < len(bundle) else xp
            return name, emoji, quote, next_min
    # Если почему-то не нашли — фолбэк на последнюю запись
    lo, hi, name, emoji, quote = bundle[-1]
    return name, emoji, quote, xp


# --- queries -----------------------------------------------------------------

async def get_user_achievements_count(user_id: int) -> int:
    """Возвращает количество достижений, полученных пользователем."""
    try:
        count = await database.fetch_val(
            "SELECT COUNT(*) FROM achievements WHERE user_id = :uid",
            {"uid": user_id}
        )
        return count or 0
    except Exception:
        logger.exception(f"Не удалось получить количество достижений для user_id={user_id}")
        return 0

async def get_user_stats(user_id: int) -> dict:
    """Загружает статистику пользователя из БД."""
    logger.debug(f"get_user_stats: загрузка статистики для user_id={user_id}")
    try:
        row = await database.fetch_one("""
            SELECT
                xp_balance,
                created_at,
                special_reward,
                finished_habits,
                finished_challenges,
                active_days,
                current_streak,
                best_streak
            FROM users
            WHERE user_id = :user_id
        """, {"user_id": user_id})

        if not row:
            return {
                "xp": 0,
                "created_at": None,
                "reward_received": False,
                "finished_habits": 0,
                "finished_challenges": 0,
                "active_days": 0,
                "current_streak": 0,
                "best_streak": 0,
            }

        return {
            "xp": row["xp_balance"],
            "created_at": row["created_at"],
            "reward_received": bool(row["special_reward"]),
            "finished_habits": row["finished_habits"],
            "finished_challenges": row["finished_challenges"],
            "active_days": row["active_days"],
            "current_streak": row["current_streak"],
            "best_streak": row["best_streak"],
        }

    except Exception:
        logger.exception(f"get_user_stats: ошибка при загрузке статистики для user_id={user_id}")
        return {
            "xp": 0,
            "created_at": None,
            "reward_received": False,
            "finished_habits": 0,
            "finished_challenges": 0,
            "active_days": 0,
            "current_streak": 0,
            "best_streak": 0,
        }

# --- view --------------------------------------------------------------------

async def send_stats(target, user_id: int, username: str | None):
    """Формирует и отправляет сообщение со статистикой (i18n)."""
    logger.info(f"send_stats: подготовка статистики для user_id={user_id}, username={username}")
    try:
        lang = await _get_lang(user_id)
        T = STATISTICS_TEXTS.get(lang, STATISTICS_TEXTS["ru"])

        stats = await get_user_stats(user_id)
        league_name, emoji, quote, next_level_xp = _get_league_i18n(stats["xp"], lang)

        current_xp = stats["xp"]
        xp_to_next = max(0, next_level_xp - current_xp)

        created = stats["created_at"].strftime("%d.%m.%Y") if stats["created_at"] else "-"
        reward = "✅" if stats["reward_received"] else "❌"
        user_achievements = await get_user_achievements_count(user_id)
        uname = (username or T["no_username"]).lstrip("@")

        text = (
            f"{T['stats_title']}\n"
            f"@{uname}\n\n"
            f"{T['league'].format(emoji=emoji, league=league_name, xp=current_xp, xp_to_next=xp_to_next)}\n"
            f"{T['current_streak'].format(days=stats['current_streak'])}\n"
            f"{T['best_streak'].format(days=stats['best_streak'])}\n"
            f"{T['active_days'].format(days=stats['active_days'])}\n\n"
            f"{T['finished_habits'].format(count=stats['finished_habits'])}\n"
            f"{T['finished_challenges'].format(count=stats['finished_challenges'])}\n"
            f"{T['achievements'].format(have=user_achievements, total=TOTAL_ACHIEVEMENTS)}\n\n"
            f"{T['reward'].format(value=reward)}\n"
            f"{T['created_at'].format(date=created)}\n\n"
            f"<em>“{quote}”</em>"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=T["back"], callback_data="back_to_about")]
        ])

        await safe_replace_message(
            target,
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        logger.info(f"send_stats: статистика отправлена user_id={user_id}")
    except Exception:
        logger.exception(f"send_stats: не удалось отправить статистику для user_id={user_id}")

# --- handlers ----------------------------------------------------------------

_STATS_VARIANTS = _stats_variants()

@router.message(lambda m: (m.text or "") in _STATS_VARIANTS)
async def handle_stats_message(message: types.Message):
    await send_stats(message, message.from_user.id, message.from_user.username)

@router.callback_query(F.data == "about_stats")
async def handle_stats_callback(callback: types.CallbackQuery):
    try:
        await callback.answer()
    except TelegramBadRequest:
        pass
    await send_stats(callback.message, callback.from_user.id, callback.from_user.username)
