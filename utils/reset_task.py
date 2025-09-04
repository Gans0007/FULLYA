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
    """
    Ежедневный запуск около 00:00 Europe/Kyiv.
    Правила:
      - Первый пропуск (вчера) → предупреждение (НЕ аннулируем)
      - Второй подряд пропуск → аннулирование + уведомление
      - Если пропусков нет вообще → позитивный отчёт «всё подтверждено»
    """
    user_ids = await get_all_users_with_active_habits()
    logging.info("[RESET] старт ночного прохода: пользователей=%d", len(user_ids))

    total_first_all = 0
    total_drop_all = 0
    total_all_clear = 0

    def _fmt(names):
        # Аккуратно формируем список названий для сообщения/логов
        # (чтобы не раздувать логи, ограничим до 10 пунктов)
        if not names:
            return ""
        names = list(names)
        if len(names) > 10:
            shown = ", ".join(f"«{n}»" for n in names[:10])
            return f"{shown} и ещё {len(names) - 10}…"
        return ", ".join(f"«{n}»" for n in names)

    for user_id in user_ids:
        try:
            # Привычки
            fm_habits, dr_habits = await reset_unconfirmed_habits(user_id)
            # Челленджи
            fm_chals,  dr_chals  = await reset_unconfirmed_challenges(user_id)

            total_first = len(fm_habits) + len(fm_chals)
            total_drop  = len(dr_habits) + len(dr_chals)
            total_first_all += total_first
            total_drop_all  += total_drop

            logging.info(
                "[RESET] user_id=%s first_miss=%d dropped=%d | fm_habits=[%s] fm_chals=[%s] dr_habits=[%s] dr_chals=[%s]",
                user_id,
                total_first, total_drop,
                _fmt(fm_habits), _fmt(fm_chals),
                _fmt(dr_habits), _fmt(dr_chals),
            )

            # 1) Мягкое предупреждение — первый пропуск (НЕ аннулируем)
            if fm_habits or fm_chals:
                parts = []
                if fm_habits:
                    parts.append("• Привычки: " + _fmt(fm_habits))
                if fm_chals:
                    parts.append("• Челленджи: " + _fmt(fm_chals))

                text = (
                    "⚠️ Ты не подтвердил вчера.\n"
                    "Первый пропуск не аннулирует прогресс — всякое бывает.\n"
                    "Но сегодня нужно подтвердить, чтобы не потерять стрик завтра!\n\n"
                    + "\n".join(parts)
                )
                try:
                    await bot.send_message(user_id, text)
                except Exception as e:
                    logging.warning("[RESET] send first_miss failed user_id=%s: %r", user_id, e)

            # 2) Жёсткое уведомление — второй подряд пропуск (прогресс уже обнулён)
            if dr_habits or dr_chals:
                parts = []
                if dr_habits:
                    parts.append("• Привычки: " + _fmt(dr_habits))
                if dr_chals:
                    parts.append("• Челленджи: " + _fmt(dr_chals))

                text = (
                    "❌ Два дня без подтверждения — прогресс аннулирован.\n"
                    "Начинай заново и держи ритм. Ты справишься.\n\n"
                    + "\n".join(parts)
                )
                try:
                    await bot.send_message(user_id, text)
                except Exception as e:
                    logging.warning("[RESET] send dropped failed user_id=%s: %r", user_id, e)

            # 3) Позитивный отчёт — всё подтверждено (ни пропусков, ни аннулирований)
            if not (fm_habits or dr_habits or fm_chals or dr_chals):
                total_all_clear += 1
                ok_text = (
                    "✅ Все привычки и челленджи были подтверждены вчера.\n"
                    "Дисциплина на месте — держим темп! 💪🔥"
                )
                try:
                    await bot.send_message(user_id, ok_text)
                except Exception as e:
                    logging.warning("[RESET] send all_clear failed user_id=%s: %r", user_id, e)

        except Exception as e:
            # Ловим любые неожиданности по конкретному юзеру, чтобы не уронить весь ночной проход
            logging.exception("[RESET] ошибка обработки user_id=%s: %r", user_id, e)

    logging.info(
        "[RESET] финал ночного прохода: всего_first_miss=%d, всего_dropped=%d, all_clear=%d, пользователей=%d",
        total_first_all, total_drop_all, total_all_clear, len(user_ids)
    )



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

