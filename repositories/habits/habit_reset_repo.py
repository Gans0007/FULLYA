from datetime import datetime, timedelta
import pytz
from db.db import database

TZ = pytz.timezone("Europe/Kyiv")

async def _yesterday_dates():
    now = datetime.now(TZ)
    y = (now - timedelta(days=1)).date()          # вчера (календарная дата Киева)
    dby = (now - timedelta(days=2)).date()        # позавчера
    return y, dby

async def reset_unconfirmed_habits(user_id: int):
    """
    Возвращает кортеж списков: (warn_list, dropped_list)
    - warn_list: привычки с 1-м подряд пропуском (только предупреждение)
    - dropped_list: привычки со 2-м подряд пропуском (аннулирование + сброс done_days)
    """
    yesterday, day_before_yesterday = await _yesterday_dates()
    warn, dropped = [], []

    # Берём активные не-челлендж привычки
    habits = await database.fetch_all("""
        SELECT id, name FROM habits
        WHERE user_id = :user_id
          AND confirm_type != 'wake_time'
          AND is_active = TRUE
          AND is_challenge = FALSE
    """, {"user_id": user_id})

    for habit in habits:
        # Было ли подтверждение вчера?
        confirmed_y = await database.fetch_one("""
            SELECT 1 FROM confirmations
            WHERE user_id = :user_id
              AND habit_id = :habit_id
              AND DATE(datetime AT TIME ZONE 'Europe/Kyiv') = :yesterday
        """, {"user_id": user_id, "habit_id": habit.id, "yesterday": yesterday})

        if confirmed_y is not None:
            # Вчера подтверждал — всё ок
            continue

        # Не подтвердил вчера -> проверяем позавчера
        confirmed_dby = await database.fetch_one("""
            SELECT 1 FROM confirmations
            WHERE user_id = :user_id
              AND habit_id = :habit_id
              AND DATE(datetime AT TIME ZONE 'Europe/Kyiv') = :dby
        """, {"user_id": user_id, "habit_id": habit.id, "dby": day_before_yesterday})

        if confirmed_dby is None:
            # Позавчера тоже нет — 2-й подряд пропуск => аннулирование
            await database.execute("""
                UPDATE habits SET done_days = 0 WHERE id = :habit_id
            """, {"habit_id": habit.id})
            dropped.append(habit.name)
        else:
            # Вчера — первый пропуск => только предупреждение
            warn.append(habit.name)

    return warn, dropped


async def reset_unconfirmed_challenges(user_id: int):
    """
    Аналогично привычкам: (warn_list, dropped_list) для челленджей.
    """
    yesterday, day_before_yesterday = await _yesterday_dates()
    warn, dropped = [], []

    challenges = await database.fetch_all("""
        SELECT id, name FROM habits
        WHERE user_id = :user_id
          AND is_active = TRUE
          AND is_challenge = TRUE
    """, {"user_id": user_id})

    for challenge in challenges:
        confirmed_y = await database.fetch_one("""
            SELECT 1 FROM confirmations
            WHERE user_id = :user_id
              AND habit_id = :habit_id
              AND DATE(datetime AT TIME ZONE 'Europe/Kyiv') = :yesterday
        """, {"user_id": user_id, "habit_id": challenge.id, "yesterday": yesterday})

        if confirmed_y is not None:
            continue

        confirmed_dby = await database.fetch_one("""
            SELECT 1 FROM confirmations
            WHERE user_id = :user_id
              AND habit_id = :habit_id
              AND DATE(datetime AT TIME ZONE 'Europe/Kyiv') = :dby
        """, {"user_id": user_id, "habit_id": challenge.id, "dby": day_before_yesterday})

        if confirmed_dby is None:
            await database.execute("""
                UPDATE habits SET done_days = 0 WHERE id = :habit_id
            """, {"habit_id": challenge.id})
            dropped.append(challenge.name)
        else:
            warn.append(challenge.name)

    return warn, dropped
