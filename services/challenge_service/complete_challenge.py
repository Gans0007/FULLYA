from db.db import database
from aiogram import Bot


async def complete_challenge(habit_id: int, user_id: int, bot: Bot):
    # Получаем challenge_id перед удалением привычки
    row = await database.fetch_one("""
        SELECT challenge_id, name, days, done_days
        FROM habits
        WHERE id = :habit_id AND user_id = :user_id
    """, {"habit_id": habit_id, "user_id": user_id})

    if not row or not row["challenge_id"]:
        return

    challenge_id = row["challenge_id"]
    name = row["name"]
    total_days = row["days"]
    done_days = row["done_days"]

    # 1. Сохраняем ID выполненного челленджа
    await database.execute("""
        INSERT INTO completed_challenges (user_id, challenge_id, completed_at)
        VALUES (:user_id, :challenge_id, CURRENT_TIMESTAMP)
    """, {
        "user_id": user_id,
        "challenge_id": challenge_id
    })

    # 2. Увеличиваем счётчик завершённых челленджей
    await database.execute("""
        UPDATE users
        SET finished_challenges = finished_challenges + 1
        WHERE user_id = :user_id
    """, {"user_id": user_id})

    # 3. Удаляем привычку
    await database.execute("""
        DELETE FROM habits
        WHERE id = :habit_id AND user_id = :user_id
    """, {"habit_id": habit_id, "user_id": user_id})

    # 4. Уведомление
    await bot.send_message(
        user_id,
        f"🏆 <b>Челлендж «{name}» завершён!</b>\n\n"
        f"<b>{done_days} из {total_days} дней</b> выполнено.\n"
        f"Теперь ты можешь взять новый вызов 💪",
        parse_mode="HTML"
    )
