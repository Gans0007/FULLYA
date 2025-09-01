import asyncio
from datetime import datetime, timedelta
import pytz
from aiogram import Bot
from config import BOT_TOKEN
from pathlib import Path
import logging

from repositories.users.user_repo import get_all_users_with_active_habits
from repositories.habits.habit_reset_repo import reset_unconfirmed_habits, reset_unconfirmed_challenges
from handlers.texts.notifications_texts import HABIT_RESET_MESSAGES, CHALLENGE_RESET_MESSAGES, HABIT_MISS_WARN_MESSAGES, CHALLENGE_MISS_WARN_MESSAGES
from db.db import database

RESET_FILE_PATH = Path(__file__).resolve().parent / "last_reset.txt"

logger = logging.getLogger(__name__)

def get_last_reset_date():
    if RESET_FILE_PATH.exists():
        return RESET_FILE_PATH.read_text().strip()
    return ""

def update_last_reset_date(date_str):
    RESET_FILE_PATH.write_text(date_str)

async def perform_reset(bot: Bot):
    user_ids = await get_all_users_with_active_habits()

    for user_id in user_ids:
        # стиль уведомлений пользователя
        user_row = await database.fetch_one(
            "SELECT notification_tone FROM users WHERE user_id = :uid",
            {"uid": user_id}
        )
        tone = user_row["notification_tone"] if user_row and user_row["notification_tone"] else "mixed"

        # --- Привычки ---
        warn_habits, dropped_habits = await reset_unconfirmed_habits(user_id)

        if warn_habits or dropped_habits:
            logger.info(
                f"[СБРОС][ПРИВЫЧКИ] Пользователь={user_id}, "
                f"Предупреждения={len(warn_habits)} {warn_habits}, "
                f"Аннулированы={len(dropped_habits)} {dropped_habits}"
            )

        for habit_name in warn_habits:
            try:
                await bot.send_message(
                    user_id,
                    HABIT_MISS_WARN_MESSAGES[tone].format(habit_name=habit_name),
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"[ОШИБКА][ПРИВЫЧКА] user={user_id}, habit={habit_name}, err={e}")

        for habit_name in dropped_habits:
            try:
                await bot.send_message(
                    user_id,
                    HABIT_RESET_MESSAGES[tone].format(habit_name=habit_name),
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"[ОШИБКА][ПРИВЫЧКА] user={user_id}, habit={habit_name}, err={e}")

        # --- Челленджи ---
        warn_chals, dropped_chals = await reset_unconfirmed_challenges(user_id)

        if warn_chals or dropped_chals:
            logger.info(
                f"[СБРОС][ЧЕЛЛЕНДЖИ] Пользователь={user_id}, "
                f"Предупреждения={len(warn_chals)} {warn_chals}, "
                f"Аннулированы={len(dropped_chals)} {dropped_chals}"
            )

        for challenge_name in warn_chals:
            try:
                await bot.send_message(
                    user_id,
                    CHALLENGE_MISS_WARN_MESSAGES[tone].format(challenge_name=challenge_name),
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"[ОШИБКА][ЧЕЛЛЕНДЖ] user={user_id}, chal={challenge_name}, err={e}")

        for challenge_name in dropped_chals:
            try:
                await bot.send_message(
                    user_id,
                    CHALLENGE_RESET_MESSAGES[tone].format(challenge_name=challenge_name),
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"[ОШИБКА][ЧЕЛЛЕНДЖ] user={user_id}, chal={challenge_name}, err={e}")

        # --- Ежедневный отчёт ---
        total_warn = len(warn_habits) + len(warn_chals)
        total_drop = len(dropped_habits) + len(dropped_chals)

        if total_warn == 0 and total_drop == 0:
            summary_text = (
                "✅ Ночной чек выполнен.\n"
                "Пропусков нет — держишь темп! 💪"
            )
        else:
            lines = ["🗓 <b>Итоги ночного чека</b>:"]
            if warn_habits:
                lines.append("• ⚠️ Предупреждения по привычкам: " + ", ".join(warn_habits))
            if dropped_habits:
                lines.append("• ⛔️ Аннулированы привычки: " + ", ".join(dropped_habits))
            if warn_chals:
                lines.append("• ⚠️ Предупреждения по челленджам: " + ", ".join(warn_chals))
            if dropped_chals:
                lines.append("• ⛔️ Аннулированы челленджи: " + ", ".join(dropped_chals))
            lines.append(f"\nИтого: предупреждений — {total_warn}, аннулирований — {total_drop}.")
            summary_text = "\n".join(lines)

        try:
            await bot.send_message(user_id, summary_text, parse_mode="HTML")
            logger.info(f"[СБРОС][ОТЧЁТ] user={user_id}, warn={total_warn}, drop={total_drop}")
        except Exception as e:
            logger.error(f"[СБРОС][ОТЧЁТ][ОШИБКА] user={user_id}: {e}")

    # отметка последнего сброса
    update_last_reset_date(datetime.now(pytz.timezone("Europe/Kyiv")).date().isoformat())



async def start_reset_scheduler(bot: Bot):
    """
    Планировщик сброса: запускается ТОЛЬКО в 00:00 по Киеву.
    При старте бота никакого сброса не выполняется.
    """
    tz = pytz.timezone("Europe/Kyiv")

    while True:
        now = datetime.now(tz)
        # ближайшая полночь
        next_reset = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        sleep_time = (next_reset - now).total_seconds()
        logging.info(f"[RESET] Сейчас {now.strftime('%Y-%m-%d %H:%M:%S')}, засыпаю до полуночи ({next_reset.strftime('%Y-%m-%d %H:%M:%S')})")

        if sleep_time > 0:
            await asyncio.sleep(sleep_time)

        logging.info("[RESET] Проснулся в полночь, готовлюсь к сбросу…")
        await asyncio.sleep(5)  # задержка для стабильности

        # защита от повторов
        today_str = datetime.now(tz).date().isoformat()
        last_reset = get_last_reset_date()
        if last_reset != today_str:
            logging.info(f"[RESET] Выполняю сброс привычек/челленджей за {today_str}")
            await perform_reset(bot)
            logging.info(f"[RESET] Сброс завершён за {today_str}")
        else:
            logging.info(f"[RESET] Сброс за {today_str} уже был выполнен ранее, пропускаю")

