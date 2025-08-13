import asyncio
import logging
import os
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from init_pg_db import init_postgres_db
from routers_register import register_all_routers
from middlewares.db import DatabaseMiddleware
from services.reminder.reminder import (
    scheduled_reminder_loop,
    scheduled_goal_dream_reminders,
)
from utils.reset_task import start_reset_scheduler

from db.db import database, DATABASE_URL


# ─────────────────────────────
# ЛОГИ
# ─────────────────────────────
os.makedirs("logs", exist_ok=True)

# общий формат
FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
formatter = logging.Formatter(FORMAT)

# основной лог с ротацией
file_handler = RotatingFileHandler(
    "logs/bot.log", maxBytes=2_000_000, backupCount=5, encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# критический лог
crit_handler = RotatingFileHandler(
    "logs/critical.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8"
)
crit_handler.setLevel(logging.ERROR)
crit_handler.setFormatter(formatter)

# консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, crit_handler, console_handler])
logger = logging.getLogger("bot")


# ─────────────────────────────
# BOT & DISPATCHER
# ─────────────────────────────
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# middleware (БД в хэндлерах)
dp.message.middleware(DatabaseMiddleware())
dp.callback_query.middleware(DatabaseMiddleware())


async def main():
    logger.info("🚀 Запуск бота...")
    logger.info(f"📡 DATABASE_URL detected: {DATABASE_URL!r}")

    # Подключение к БД и проверка схемы
    await database.connect()
    logger.info("📦 Подключение к PostgreSQL установлено.")
    await init_postgres_db()
    logger.info("🛠 Таблицы проверены/созданы (init_postgres_db).")

    # Роутеры
    await register_all_routers(dp)
    logger.info("🔁 Роутеры зарегистрированы.")

    # Фоновые задачи (сохраняем ссылки — для корректной остановки)
    bg_tasks = [
        asyncio.create_task(scheduled_reminder_loop(bot), name="scheduled_reminder_loop"),
        asyncio.create_task(scheduled_goal_dream_reminders(bot), name="scheduled_goal_dream_reminders"),
        asyncio.create_task(start_reset_scheduler(bot), name="start_reset_scheduler"),
    ]
    logger.info("⏰ Планировщики запущены.")

    try:
        # Старт поллинга (обрабатывает SIGINT/SIGTERM внутри)
        await dp.start_polling(bot)
    finally:
        # Graceful shutdown фоновых задач
        logger.info("🛑 Остановка: отменяем фоновые задачи...")
        for t in bg_tasks:
            t.cancel()
        results = await asyncio.gather(*bg_tasks, return_exceptions=True)
        for name, res in zip((t.get_name() for t in bg_tasks), results):
            if isinstance(res, Exception):
                logger.error("Фоновая задача %s завершилась с ошибкой: %r", name, res)
            else:
                logger.info("Фоновая задача %s завершилась корректно.", name)

        # Отключение от БД
        await database.disconnect()
        logger.info("📴 PostgreSQL отключён.")

        logger.info("👋 Бот остановлен.")


if __name__ == "__main__":
    asyncio.run(main())
