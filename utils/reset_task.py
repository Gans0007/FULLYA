import asyncio
from datetime import datetime, timedelta
import pytz
from aiogram import Bot
from config import BOT_TOKEN
from pathlib import Path

from repositories.users.user_repo import get_all_users_with_active_habits
from repositories.habits.habit_reset_repo import reset_unconfirmed_habits, reset_unconfirmed_challenges
from handlers.texts.notifications_texts import HABIT_RESET_MESSAGES, CHALLENGE_RESET_MESSAGES
from db.db import database

RESET_FILE_PATH = Path(__file__).resolve().parent / "last_reset.txt"

def get_last_reset_date():
    if RESET_FILE_PATH.exists():
        return RESET_FILE_PATH.read_text().strip()
    return ""

def update_last_reset_date(date_str):
    RESET_FILE_PATH.write_text(date_str)

async def perform_reset(bot: Bot):
    user_ids = await get_all_users_with_active_habits()

    for user_id in user_ids:
        # Получаем стиль уведомлений пользователя
        user_row = await database.fetch_one(
            "SELECT notification_tone FROM users WHERE user_id = :uid",
            {"uid": user_id}
        )
        tone = user_row["notification_tone"] if user_row and user_row["notification_tone"] else "mixed"

        # Сброс неподтверждённых привычек
        dropped_habits = await reset_unconfirmed_habits(user_id)
        if dropped_habits:
            for habit_name in dropped_habits:
                try:
                    await bot.send_message(
                        user_id,
                        HABIT_RESET_MESSAGES[tone].format(habit_name=habit_name),
                        parse_mode="HTML"
                    )
                except:
                    pass  # игнорировать ошибки отправки

        # Сброс неподтверждённых челленджей
        dropped_challenges = await reset_unconfirmed_challenges(user_id)
        if dropped_challenges:
            for challenge_name in dropped_challenges:
                try:
                    await bot.send_message(
                        user_id,
                        CHALLENGE_RESET_MESSAGES[tone].format(challenge_name=challenge_name),
                        parse_mode="HTML"
                    )
                except:
                    pass  # игнорировать ошибки отправки

    update_last_reset_date(datetime.now(pytz.timezone("Europe/Kyiv")).date().isoformat())

async def start_reset_scheduler(bot: Bot):
    # 🔁 При запуске — проверка, не пропущен ли сброс
    now = datetime.now(pytz.timezone("Europe/Kyiv"))
    today_str = now.date().isoformat()
    last_reset = get_last_reset_date()

    if last_reset != today_str and now.time().hour >= 0:
        await perform_reset(bot)

    while True:
        now = datetime.now(pytz.timezone("Europe/Kyiv"))
        next_reset = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if now >= next_reset:
            next_reset += timedelta(days=1)
        sleep_time = (next_reset - now).total_seconds()

        await asyncio.sleep(sleep_time)
        await perform_reset(bot)
