from aiogram import Bot
from utils.timezones import get_current_time
from db.db import database
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


async def log_confirmation(user_id: int, habit_id: int, file_id: str, file_type: str, bot: Bot):
    now = get_current_time()
    today = now.date()

    # Получаем дату последнего подтверждения
    row = await database.fetch_one("""
        SELECT current_streak, best_streak, last_confirmation_date
        FROM users WHERE user_id = :user_id
    """, {"user_id": user_id})
    last_date = row["last_confirmation_date"] if row else None
    current_streak = row["current_streak"] if row else 0
    best_streak = row["best_streak"] if row else 0

    logger.info(f"[CONFIRMATION] last_date={last_date}, today={today} для user_id={user_id}")

    new_active_day = last_date != today

    if new_active_day:
        # --- Подсчет стрика ---
        from datetime import datetime, timedelta
        if isinstance(last_date, str):
            last_date = datetime.strptime(last_date, "%Y-%m-%d").date() if last_date else None

        yesterday = today - timedelta(days=1)
        if last_date == yesterday:
            current_streak += 1
        else:
            current_streak = 1

        if current_streak > best_streak:
            best_streak = current_streak

        # обновляем streak, active_days и last_confirmation_date
        await database.execute("""
            UPDATE users
            SET active_days = active_days + 1,
                current_streak = :current_streak,
                best_streak = :best_streak,
                last_confirmation_date = (NOW() AT TIME ZONE 'UTC')::date
            WHERE user_id = :user_id
        """, {
            "user_id": user_id,
            "current_streak": current_streak,
            "best_streak": best_streak
        })
        logger.info(f"[CONFIRMATION] ✅ Обновили активность и streak пользователя {user_id}")

    # Вставляем подтверждение — берем время на стороне БД
    await database.execute("""
        INSERT INTO confirmations (user_id, habit_id, datetime, file_id, file_type, confirmed)
        VALUES (:user_id, :habit_id, (NOW() AT TIME ZONE 'UTC'), :file_id, :file_type, :confirmed)
    """, {
        "user_id": user_id,
        "habit_id": habit_id,
        "file_id": file_id,
        "file_type": file_type,
        "confirmed": True
    })
    logger.info(f"[CONFIRMATION] ✅ Сохранили подтверждение habit_id={habit_id} для user_id={user_id}")

    if new_active_day:
        row = await database.fetch_one("""
            SELECT active_days FROM users WHERE user_id = :user_id
        """, {"user_id": user_id})
        active_days = row["active_days"] if row else 0
        logger.info(f"[CONFIRMATION] У пользователя {user_id} сейчас {active_days} active_days")

        if active_days == 3:
            row = await database.fetch_one("""
                SELECT is_active FROM referrals WHERE invited_id = :user_id
            """, {"user_id": user_id})
            logger.info(f"[DEBUG] Запись в referrals для {user_id}: {row}")

            if row and row["is_active"] == 0:
                await database.execute("""
                    UPDATE referrals SET is_active = TRUE WHERE invited_id = :user_id
                """, {"user_id": user_id})
                logger.info(f"[REFERRAL] 🎯 Обновили is_active для {user_id}")

    # === ДОБАВЛЕНО: выдача ачивок ===
    from handlers.achievements import check_and_grant

    # 1. Подтверждения (habit_done)
    total_confirms = await database.fetch_val(
        "SELECT COUNT(*) FROM confirmations WHERE user_id = :uid",
        {"uid": user_id}
    )
    logger.info(f"[ACHIEVEMENTS] Подтверждений у user_id={user_id}: {total_confirms}")
    await check_and_grant(user_id, "habit_done", total_confirms, bot)

    # 2. Стрики (streak)
    streak_count = await database.fetch_val(
        "SELECT current_streak FROM users WHERE user_id = :uid",
        {"uid": user_id}
    )
    logger.info(f"[ACHIEVEMENTS] Текущий стрик user_id={user_id}: {streak_count}")
    if streak_count:
        await check_and_grant(user_id, "streak", streak_count, bot)

    # 3. Активные дни (active_days)
    active_days = await database.fetch_val(
        "SELECT active_days FROM users WHERE user_id = :uid",
        {"uid": user_id}
    )
    logger.info(f"[ACHIEVEMENTS] Активных дней у user_id={user_id}: {active_days}")
    if active_days:
        await check_and_grant(user_id, "active_days", active_days, bot)



async def was_confirmed_today(user_id: int, habit_id: int) -> bool:
    # Сверяем по дате в UTC на стороне БД
    row = await database.fetch_one("""
        SELECT 1 FROM confirmations
        WHERE user_id = :user_id
          AND habit_id = :habit_id
          AND DATE(datetime) = (NOW() AT TIME ZONE 'UTC')::date
    """, {"user_id": user_id, "habit_id": habit_id})
    return row is not None


async def update_confirmation_file(user_id: int, habit_id: int, file_id: str, file_type: str):
    # Обновляем с текущим временем БД, без передачи Python datetime
    await database.execute("""
        UPDATE confirmations
        SET datetime = (NOW() AT TIME ZONE 'UTC'),
            file_id = :file_id,
            file_type = :file_type
        WHERE user_id = :user_id
          AND habit_id = :habit_id
          AND DATE(datetime) = (NOW() AT TIME ZONE 'UTC')::date
    """, {
        "file_id": file_id,
        "file_type": file_type,
        "user_id": user_id,
        "habit_id": habit_id
    })
