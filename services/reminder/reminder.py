import asyncio
import random
import logging
from datetime import timedelta, datetime
from aiogram import Bot
from utils.timezones import get_current_time
from repositories.habits.habit_repo import get_unconfirmed_today
from repositories.users.user_repo import get_all_user_ids
from db.db import database

# ✅ импорт мультиязычных текстов
from handlers.texts.notifications_texts import REMINDER_MESSAGES, GOAL_REMINDERS, DREAM_REMINDERS

logger = logging.getLogger(__name__)

MIN_HOUR = 8
MAX_HOUR = 21

async def safe_fetch_all(query: str, values: dict = None, retries: int = 3, delay: int = 3):
    for attempt in range(retries):
        try:
            return await database.fetch_all(query, values)
        except Exception as e:
            logger.warning(f"[DB] Ошибка fetch_all (попытка {attempt+1}): {e}")
            await asyncio.sleep(delay)
    logger.error("[DB] ❌ Не удалось выполнить fetch_all после нескольких попыток")
    return []

# === 1. Привычки ===
async def scheduled_reminder_loop(bot: Bot):
    already_planned_today = False
    while True:
        try:
            now = get_current_time()

            # Планируем только один раз в день (и в 08:00 обновляем)
            if not already_planned_today or (now.hour == 8 and now.minute == 0):
                logger.info(f"[REMINDER] Планируем напоминания на {now.date()}")
                await plan_reminders_for_today(bot, now)
                already_planned_today = True

            await asyncio.sleep(60)

        except Exception as e:
            logger.exception(f"[REMINDER] Ошибка в scheduled_reminder_loop: {e}")
            await asyncio.sleep(10)


async def plan_reminders_for_today(bot: Bot, now):
    """
    Планирует отложенные задачи для всех привычек на сегодня.
    """
    user_ids = await get_all_user_ids()
    for user_id in user_ids:
        habits = await get_unconfirmed_today(user_id)
        for habit in habits:
            rand_hour = random.randint(MIN_HOUR, MAX_HOUR)
            rand_min = random.randint(0, 59)
            send_time = now.replace(hour=rand_hour, minute=rand_min, second=0, microsecond=0)
            if send_time <= now:
                send_time += timedelta(days=1)

            delay = (send_time - now).total_seconds()
            logger.info(f"[REMINDER] habit_id={habit.id}, user_id={user_id} на {send_time.strftime('%H:%M')}")
            asyncio.create_task(send_delayed_reminder(bot, user_id, habit, delay))


async def send_delayed_reminder(bot: Bot, user_id: int, habit, delay: float):
    try:
        await asyncio.sleep(delay)

        # Проверяем, что привычка всё ещё не подтверждена
        updated = await get_unconfirmed_today(user_id)
        if not any(h.id == habit.id for h in updated):
            return

        # Получаем язык и стиль уведомлений пользователя
        user_row = await database.fetch_one(
            "SELECT language, notification_tone FROM users WHERE user_id = :uid",
            {"uid": user_id}
        )
        lang = (user_row["language"] if user_row and user_row["language"] in REMINDER_MESSAGES else "ru")
        tone = (user_row["notification_tone"] if user_row and user_row["notification_tone"] else "mixed")

        # Выбираем подходящее сообщение
        tone_dict = REMINDER_MESSAGES.get(lang, REMINDER_MESSAGES["ru"])
        tone_list = tone_dict.get(tone, tone_dict.get("mixed", REMINDER_MESSAGES["ru"]["mixed"]))
        message_template = random.choice(tone_list)
        text = message_template.format(name=habit.name, done=habit.done_days, total=habit.days)

        await bot.send_message(user_id, text)

    except Exception as e:
        logger.exception(f"[REMINDER] Ошибка при отправке пользователю {user_id}: {e}")


# === 2. Цели и мечты ===
async def scheduled_goal_dream_reminders(bot: Bot):
    while True:
        try:
            now = datetime.utcnow()
            users = await safe_fetch_all("""
                SELECT user_id, language, goals_reminder_at, dreams_reminder_at
                FROM users
            """)

            for user in users:
                uid = user["user_id"]
                lang = user["language"] if user["language"] in GOAL_REMINDERS else "ru"

                # === ЦЕЛИ ===
                if not user["goals_reminder_at"] or user["goals_reminder_at"] <= now:
                    goal = await database.fetch_one("""
                        SELECT id, text FROM goals
                        WHERE user_id = :uid AND is_done = false
                        ORDER BY random() LIMIT 1
                    """, {"uid": uid})
                    if goal:
                        try:
                            goal_tpl = random.choice(GOAL_REMINDERS[lang])
                            await bot.send_message(uid, goal_tpl.format(text=goal["text"]))
                            await database.execute(
                                "UPDATE users SET goals_reminder_at = :next WHERE user_id = :uid",
                                {"next": now + timedelta(days=16), "uid": uid}
                            )
                        except Exception as e:
                            logger.warning(f"[REMINDER] Ошибка при отправке цели: {e}")

                # === МЕЧТЫ ===
                if not user["dreams_reminder_at"] or user["dreams_reminder_at"] <= now:
                    dream = await database.fetch_one("""
                        SELECT id, text FROM dreams
                        WHERE user_id = :uid AND is_done = false
                        ORDER BY random() LIMIT 1
                    """, {"uid": uid})
                    if dream:
                        try:
                            dream_tpl = random.choice(DREAM_REMINDERS[lang])
                            await bot.send_message(uid, dream_tpl.format(text=dream["text"]))
                            await database.execute(
                                "UPDATE users SET dreams_reminder_at = :next WHERE user_id = :uid",
                                {"next": now + timedelta(days=30), "uid": uid}
                            )
                        except Exception as e:
                            logger.warning(f"[REMINDER] Ошибка при отправке мечты: {e}")

            await asyncio.sleep(60)

        except Exception as e:
            logger.exception(f"[REMINDER] ❌ Ошибка в scheduled_goal_dream_reminders: {e}")
            await asyncio.sleep(10)
