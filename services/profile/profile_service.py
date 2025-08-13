# services/profile/profile_service.py

from typing import Tuple
from db.db import database
from handlers.texts.achievements_texts import LIGAS as LIGAS_TEXTS


async def get_lang(user_id: int) -> str:
    """
    Возвращает язык интерфейса пользователя (ru/uk/en).
    Фолбэк — 'ru', если язык не задан или отсутствует в LIGAS_TEXTS.
    """
    # Record не поддерживает .get(), поэтому берём сразу значение
    lang_val = await database.fetch_val(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id},
    )
    lang = (lang_val or "ru").lower()
    return lang if lang in LIGAS_TEXTS else "ru"


def _get_ligas_for_lang(lang: str):
    """
    Возвращает таблицу лиг для нужного языка.
    Формат элемента: (low, high, name, emoji, quote)
    """
    return LIGAS_TEXTS.get(lang) or LIGAS_TEXTS["ru"]


def get_liga_by_xp(xp: int, lang: str = "ru") -> Tuple[str, str, str, int]:
    """
    Возвращает (название_лиги, эмодзи, цитата, порог_следующего_уровня) для заданного XP и языка.
    """
    ligas = _get_ligas_for_lang(lang)

    for i, (low, high, name, emoji, quote) in enumerate(ligas):
        if low <= xp <= high:
            next_level_xp = ligas[i + 1][0] if i + 1 < len(ligas) else high
            return name, emoji, quote, next_level_xp

    # На всякий случай (вне диапазонов)
    last_high = ligas[-1][1] if ligas else 0
    return "—", "❔", "", last_high


async def get_user_profile_summary(user_id: int) -> Tuple[float, int, str, str]:
    """
    Возвращает кортеж:
      (usdt_balance, xp_balance, liga_title, liga_quote)
    """
    lang = await get_lang(user_id)

    row = await database.fetch_one(
        """
        SELECT xp_balance, usdt_balance
        FROM users
        WHERE user_id = :user_id
        """,
        {"user_id": user_id},
    )
    # Record -> dict, чтобы можно было .get()
    d = dict(row) if row else {}
    xp = d.get("xp_balance") or 0
    usdt = d.get("usdt_balance") or 0.0

    liga_name, emoji, liga_quote, _ = get_liga_by_xp(xp, lang)
    liga_title = f"{emoji} {liga_name}".strip()

    return usdt, xp, liga_title, liga_quote


# Ре-экспорт для обратной совместимости, если где-то ещё импортируют LIGAS из profile_service
LIGAS = LIGAS_TEXTS
