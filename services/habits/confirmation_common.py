import random
from repositories.habits.habit_repo import get_habit_by_id
from services.confirmations.confirmation_service import process_confirmation, send_to_public_chat
from services.challenge_service.complete_challenge import complete_challenge
from services.profile import xp_service
from handlers.texts.notifications_texts import CONFIRM_MESSAGES, SPECIAL_REWARD_MESSAGE
from db.db import database


async def confirm_media_habit(user, habit_id: int, file_id: str, file_type: str, bot):
    """
    Общая логика подтверждения привычки через медиа.
    Используется и для кнопки, и для авто-подтверждения.
    """
    habit = await get_habit_by_id(habit_id)
    if not habit:
        return "❌ Привычка не найдена."

    # Проверка времени для wake_time
    if habit.confirm_type == "wake_time":
        from services.habits.habit_confirmation_service import check_wake_time
        ok, error = await check_wake_time(habit.name)
        if not ok:
            return error

    # Подтверждаем прогресс
    progress_increased = await process_confirmation(
        user_id=user.id,
        habit_id=habit_id,
        file_id=file_id,
        file_type=file_type,
        bot=bot
    )

    # --- Публикация в паблик-чат только если включено в настройках ---
    should_share = await database.fetch_val(
        "SELECT share_confirmation_media FROM users WHERE user_id = :uid",
        {"uid": user.id}
    )
    if should_share is None:
        should_share = True  # fallback по умолчанию

    if should_share and file_id and file_type:
        # Отправляем в паблик-чат (асинхронно)
        await send_to_public_chat(
            user=user,
            habit_id=habit_id,
            file_id=file_id,
            file_type=file_type,
            bot=bot
        )

    if progress_increased:
        # +1 XP
        await xp_service.xp_for_confirmation(user.id, bot)
        await bot.send_message(user.id, "🏵 +1 XP за подтверждение привычки!")

        habit = await get_habit_by_id(habit_id)
        if habit.is_challenge and int(habit.done_days) >= int(habit.days):
            await complete_challenge(habit_id, user.id, bot)
            await xp_service.xp_for_completed_challenge(user.id, bot)
            await bot.send_message(user.id, "🏵 +5 XP за завершение челленджа!")

            from handlers.achievements import check_and_grant
            finished_challenges = await database.fetch_val(
                "SELECT finished_challenges FROM users WHERE user_id = :uid",
                {"uid": user.id}
            )
            await check_and_grant(user.id, "challenge_done", finished_challenges, bot)

        # --- Получаем язык пользователя и тон уведомлений ---
        user_data = await database.fetch_one(
            """
            SELECT active_days, special_reward, notification_tone, language 
            FROM users 
            WHERE user_id = :uid
            """,
            {"uid": user.id}
        )

        if user_data:
            active_days = user_data["active_days"]
            special_reward = user_data["special_reward"]
            tone = user_data["notification_tone"] or "mixed"
            lang = user_data["language"] or "ru"

            # special reward
            if active_days == 31 and not special_reward:
                await database.execute(
                    "UPDATE users SET special_reward = TRUE WHERE user_id = :uid",
                    {"uid": user.id}
                )
                await bot.send_message(
                    user.id,
                    SPECIAL_REWARD_MESSAGE.get(lang, SPECIAL_REWARD_MESSAGE["ru"])
                )

            # возвращаем подтверждающее сообщение на нужном языке
            return random.choice(
                CONFIRM_MESSAGES.get(tone, CONFIRM_MESSAGES["mixed"]).get(lang, CONFIRM_MESSAGES["mixed"]["ru"])
            )

    else:
        return "♻️ Медиа обновлено! Прогресс не изменён."

