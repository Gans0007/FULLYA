from db.db import database
from services.profile.profile_service import get_liga_by_xp, get_lang
from handlers.texts.achievements_texts import LIGAS as LIGAS_TEXTS
from handlers.achievements import check_and_grant


async def add_xp(user_id: int, amount: int, bot, reason: str = ""):
    """
    Универсальная функция начисления XP.
    1) Увеличивает XP пользователя.
    2) Логирует начисление в reward_history.
    3) Проверяет лигу по текущему языку пользователя.
    4) Выдаёт ачивку за новую лигу (лишь с 2-й и выше).
    """
    if amount <= 0:
        return None

    # 1) Увеличиваем XP и получаем новое значение
    new_xp = await database.fetch_val(
        """
        UPDATE users
        SET xp_balance = xp_balance + :amount
        WHERE user_id = :uid
        RETURNING xp_balance
        """,
        {"uid": user_id, "amount": amount}
    )
    if new_xp is None:
        return None

    # 2) Логируем начисление в reward_history
    await database.execute(
        """
        INSERT INTO reward_history (user_id, amount, type, reason)
        VALUES (:user_id, :amount, 'xp', :reason)
        """,
        {"user_id": user_id, "amount": amount, "reason": reason or "xp_reward"}
    )

    # 3) Определяем язык и набор лиг
    lang = await get_lang(user_id)
    ligas = LIGAS_TEXTS.get(lang, LIGAS_TEXTS["ru"])

    # (опционально) получаем текущую лигу/цитату — если используешь где-то далее
    liga_name, emoji, liga_quote, _ = get_liga_by_xp(new_xp, lang)

    # 4) Находим, в какую лигу попал пользователь и выдаём ачивку
    # Индекс 0 = «Начинающий» (нет ачивки), индекс 1 = 2-я лига (есть ачивка)
    for idx, (low, high, name, _, _) in enumerate(ligas):
        if low <= new_xp <= high:
            if idx >= 1:
                league_num = idx + 1  # idx=1 -> 2-я лига, ..., idx=9 -> 10-я лига
                await check_and_grant(user_id, "league", league_num, bot)
            break

    return new_xp


# === USDT-награды ===

async def add_usdt(user_id: int, amount: float = 1.0, reason: str = "referral_paid"):
    """
    Начисление USDT пользователю и логирование в reward_history.
    """
    if amount <= 0:
        return None

    # Обновляем баланс
    await database.execute(
        """
        UPDATE users
        SET usdt_balance = usdt_balance + :amount
        WHERE user_id = :user_id
        """,
        {"user_id": user_id, "amount": amount}
    )

    # Логируем в reward_history
    await database.execute(
        """
        INSERT INTO reward_history (user_id, amount, type, reason)
        VALUES (:user_id, :amount, 'usdt', :reason)
        """,
        {"user_id": user_id, "amount": amount, "reason": reason}
    )

    return amount


# === Утилиты для разных событий ===

# Подтверждение уникальной привычки +1 XP 🏵
async def xp_for_confirmation(user_id: int, bot):
    return await add_xp(user_id, 1, bot, reason="habit_confirmation")

# Завершение привычки +5 XP 🏵
async def xp_for_completed_habit(user_id: int, bot):
    return await add_xp(user_id, 5, bot, reason="habit_completed")

# Завершение челленджа +5 XP 🏵
async def xp_for_completed_challenge(user_id: int, bot):
    return await add_xp(user_id, 5, bot, reason="challenge_completed")

# Продление привычки +2 🏵
async def xp_for_extend_habit(user_id: int, bot):
    return await add_xp(user_id, 2, bot, reason="habit_extended")

# Достижения +2 XP
async def xp_for_achievement(user_id: int, bot):
    # чтобы избежать циклических импортов — используем локальный вызов
    return await add_xp(user_id, 2, bot, reason="achievement")

# За рефералов +1 XP
async def xp_for_referral(user_id: int, bot):
    return await add_xp(user_id, 1, bot, reason="referral")
