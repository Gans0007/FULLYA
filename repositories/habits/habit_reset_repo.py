from datetime import datetime, timedelta
import pytz
from db.db import database

TZ = pytz.timezone("Europe/Kyiv")

async def _collect_items(user_id: int, is_challenge: bool):
    # Активные привычки/челленджи (включая wake_time)
    return await database.fetch_all("""
        SELECT id, name
        FROM habits
        WHERE user_id = :user_id
          AND is_active = TRUE
          AND is_challenge = :is_challenge
    """, {"user_id": user_id, "is_challenge": is_challenge})


async def _fetch_confirmed_set(user_id: int, habit_ids: list[int], target_date):
    """
    Возвращает set(habit_id), у которых есть подтверждение в target_date.
    Сравнение по Киеву: DATE(datetime AT TIME ZONE 'Europe/Kyiv')
    """
    if not habit_ids:
        return set()

    rows = await database.fetch_all("""
        SELECT DISTINCT habit_id
        FROM confirmations
        WHERE user_id = :user_id
          AND habit_id = ANY(:habit_ids)
          AND DATE(datetime AT TIME ZONE 'Europe/Kyiv') = :day_date
    """, {"user_id": user_id, "habit_ids": habit_ids, "day_date": target_date})
    # databases возвращает маппинги -> обращаемся по строковому ключу
    return {row["habit_id"] for row in rows}

async def _process_block(user_id: int, is_challenge: bool):
    """
    Логика:
      - Если ВЧЕРА подтверждения НЕТ и ПОЗАВЧЕРА ТОЖЕ НЕТ → обнулить (dropped)
      - Если ВЧЕРА НЕТ, а ПОЗАВЧЕРА БЫЛО → только предупредить (first_miss)
      - Если ВЧЕРА БЫЛО → ничего не делаем
    """
    today = datetime.now(KYIV_TZ).date()
    yesterday = today - timedelta(days=1)
    day_before = today - timedelta(days=2)

    items = await _collect_items(user_id, is_challenge)
    if not items:
        return [], []

    habit_ids = [it["id"] for it in items]

    # ДВА батч-запроса вместо N
    confirmed_yesterday = await _fetch_confirmed_set(user_id, habit_ids, yesterday)
    confirmed_day_before = await _fetch_confirmed_set(user_id, habit_ids, day_before)

    first_miss, dropped = [], []

    for it in items:
        hid = it["id"]
        name = it["name"]

        if hid in confirmed_yesterday:
            continue  # вчера подтверждено — всё ок

        # вчера НЕ подтверждено
        if hid in confirmed_day_before:
            # первый пропуск
            first_miss.append(name)
        else:
            # второй подряд пропуск — аннулируем прогресс
            await database.execute("""
                UPDATE habits
                SET done_days = 0
                WHERE id = :habit_id
            """, {"habit_id": hid})
            dropped.append(name)

    return first_miss, dropped

async def reset_unconfirmed_habits(user_id: int):
    """Возвращает (first_miss_habits, dropped_habits)"""
    return await _process_block(user_id, is_challenge=False)

async def reset_unconfirmed_challenges(user_id: int):
    """Возвращает (first_miss_challenges, dropped_challenges)"""
    return await _process_block(user_id, is_challenge=True)
