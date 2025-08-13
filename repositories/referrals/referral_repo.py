from aiogram import Bot
from db.db import database
from utils.timezones import get_current_time
from handlers.achievements import check_and_grant
from handlers.texts.notifications_texts import JOIN_MESSAGES
import random
import logging

logger = logging.getLogger(__name__)

# --- Вспомогательное: нормализация и безопасный выбор языка ---
def _normalize_lang(lang: str | None) -> str:
    """Нормализуем язык пользователя к одному из ключей сообщений."""
    if not lang:
        return "ru"
    lang = lang.lower()
    if lang in {"ru", "en", "uk", "ua"}:
        return lang
    return "ru"

def _pick_lang_for_messages(lang: str) -> str:
    """
    Подбирает доступный ключ в JOIN_MESSAGES с фолбэками.
    Принимает 'uk' и 'ua' как взаимозаменяемые, затем ru -> en.
    """
    candidates = [lang]
    if lang == "uk":
        candidates.append("ua")
    elif lang == "ua":
        candidates.append("uk")
    candidates += ["ru", "en"]

    for key in candidates:
        if key in JOIN_MESSAGES:
            return key
    # На всякий — вернём любой первый доступный
    return next(iter(JOIN_MESSAGES.keys()))

async def _get_user_language(user_id: int) -> str:
    row = await database.fetch_one(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id}
    )
    lang = _normalize_lang(row["language"] if row else None)
    key = _pick_lang_for_messages(lang)
    if key != lang:
        logger.info(f"[REFERRAL][LANG] Requested '{lang}', using '{key}' (fallback).")
    return key

async def save_referral(referrer_id: int, invited_id: int, bot: Bot):
    if referrer_id == invited_id:
        logger.info(f"[REFERRAL] ❌ Пользователь {invited_id} попытался пригласить сам себя")
        return

    existing = await database.fetch_one(
        "SELECT 1 FROM referrals WHERE invited_id = :invited_id",
        {"invited_id": invited_id}
    )
    if existing:
        logger.info(f"[REFERRAL] ⚠️ Пользователь {invited_id} уже есть в базе — не сохраняем повторно")
        return

    query = """
        INSERT INTO referrals (referrer_id, invited_id, created_at)
        VALUES (:referrer_id, :invited_id, :created_at)
    """
    values = {
        "referrer_id": referrer_id,
        "invited_id": invited_id,
        "created_at": get_current_time()
    }
    await database.execute(query=query, values=values)

    # === Проверка достижений за рефералов ===
    total_referrals = await database.fetch_val(
        "SELECT COUNT(*) FROM referrals WHERE referrer_id = :uid",
        {"uid": referrer_id}
    )
    await check_and_grant(referrer_id, "invite", total_referrals, bot)

    # === Уведомляем пригласившего сразу после сохранения ===
    try:
        invited_user = await bot.get_chat(invited_id)

        # Язык пригласившего
        lang_key = await _get_user_language(referrer_id)
        templates = JOIN_MESSAGES.get(lang_key) or JOIN_MESSAGES.get("ru") or []
        if not templates:
            # На крайний случай, чтобы не упасть
            templates = ["🔥 Новый участник: <b>{name}</b>"]

        msg = random.choice(templates).format(name=invited_user.full_name)
        await bot.send_message(referrer_id, msg, parse_mode="HTML")
        logger.info(
            f"[REFERRAL] Уведомили пригласившего {referrer_id} о новом пользователе {invited_id} (lang={lang_key})"
        )
    except Exception as e:
        logger.warning(f"[REFERRAL] Не удалось уведомить пригласившего: {e}")

    logger.info(f"[REFERRAL] ✅ Сохранена связь: {referrer_id} → {invited_id}")


async def get_referral_stats(referrer_id: int) -> tuple[int, int]:
    total_row = await database.fetch_one(
        "SELECT COUNT(*) as count FROM referrals WHERE referrer_id = :referrer_id",
        {"referrer_id": referrer_id}
    )
    active_row = await database.fetch_one(
        "SELECT COUNT(*) as count FROM referrals WHERE referrer_id = :referrer_id AND is_active = TRUE",
        {"referrer_id": referrer_id}
    )
    return (total_row["count"] if total_row else 0,
            active_row["count"] if active_row else 0)


async def get_referrer_id(invited_id: int):
    return await database.fetch_one(
        "SELECT referrer_id FROM referrals WHERE invited_id = :invited_id",
        {"invited_id": invited_id}
    )
