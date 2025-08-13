import logging
from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from repositories.habits.habit_repo import (
    get_habit_by_id,
    delete_habit_by_id,
    complete_habit_by_id,
    extend_habit_by_id
)
from services.habits.habit_card_renderer import render_habit_card

logger = logging.getLogger(__name__)
router = Router()

# 🔹 Кнопка "Завершить привычку"
@router.callback_query(F.data.startswith("complete_habit_"))
async def handle_complete_request(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    habit_id = int(callback.data.split("_")[-1])

    try:
        habit = await get_habit_by_id(habit_id)
        if not habit:
            logger.error(f"[{user_id}] Привычка не найдена при попытке завершить (habit_id={habit_id})")
            await callback.message.answer("❌ Привычка не найдена.")
            return

        done_days = habit.done_days
        habit_name = habit.name

        logger.info(f"[{user_id}] Начал завершение привычки '{habit_name}' (дней: {done_days})")

        if done_days < 15:
            text = f"😬 У тебя меньше 15 дней по привычке «{habit_name}», она не будет учтена в статистику!"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Да", callback_data=f"confirm_remove_{habit_id}"),
                InlineKeyboardButton(text="Нет", callback_data=f"cancel_complete_{habit_id}")
            ]])
        else:
            text = f"Ты уверен, что хочешь завершить привычку «{habit_name}»?"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Да", callback_data=f"confirm_complete_{habit_id}"),
                InlineKeyboardButton(text="Нет", callback_data=f"cancel_complete_{habit_id}")
            ]])

        await callback.message.edit_text(text, reply_markup=keyboard)

    except Exception as e:
        logger.exception(f"[{user_id}] Ошибка при обработке завершения привычки habit_id={habit_id}: {e}")
        await callback.answer("Произошла ошибка", show_alert=True)

# 🔹 Подтверждение удаления привычки (менее 15 дней)
@router.callback_query(F.data.startswith("confirm_remove_"))
async def handle_remove_short_habit(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    habit_id = int(callback.data.split("_")[-1])

    try:
        await delete_habit_by_id(habit_id)
        logger.info(f"[{user_id}] Завершил привычку без статистики (habit_id={habit_id})")
        await callback.message.edit_text("⚠️ Привычка завершена, но не учтена в статистику! И всё равно ты камень 🤝")
    except Exception as e:
        logger.exception(f"[{user_id}] Ошибка при удалении привычки habit_id={habit_id}: {e}")
        await callback.answer("Произошла ошибка при удалении", show_alert=True)


# 🔹 Подтверждение завершения привычки (сохраняется)
@router.callback_query(F.data.startswith("confirm_complete_"))
async def handle_confirm_complete(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    habit_id = int(callback.data.split("_")[-1])

    try:
        from handlers.achievements import check_and_grant
        from db.db import database
        from services.profile import xp_service  # <-- добавляем импорт здесь внутри функции

        # Получаем данные привычки перед тем, как завершить её
        habit_data = await database.fetch_one(
            "SELECT name, description, days, done_days FROM habits WHERE id = :hid AND user_id = :uid",
            {"hid": habit_id, "uid": user_id}
        )

        # Отмечаем привычку завершённой (твоя логика)
        await complete_habit_by_id(habit_id)
        logger.info(f"[{user_id}] Завершил привычку с сохранением в статистику (habit_id={habit_id})")

        # Если данные привычки найдены — копируем их в таблицу completed_habits
        if habit_data:
            await database.execute("""
                INSERT INTO completed_habits (user_id, name, description, days, done_days)
                VALUES (:user_id, :name, :description, :days, :done_days)
            """, {
                "user_id": user_id,
                "name": habit_data["name"],
                "description": habit_data["description"],
                "days": habit_data["days"],
                "done_days": habit_data["done_days"]
            })
            logger.info(f"[{user_id}] Привычка сохранена в таблицу completed_habits")

        # === Проверка ачивок за завершённые привычки ===
        completed_habits = await database.fetch_val(
            "SELECT finished_habits FROM users WHERE user_id = :uid",
            {"uid": user_id}
        )
        logger.info(f"[ACHIEVEMENTS] Завершённых привычек у user_id={user_id}: {completed_habits}")
        await check_and_grant(user_id, "habit_complete", completed_habits, callback.bot)
        # ==========================================================

        # Начисляем XP за завершение привычки
        await xp_service.xp_for_completed_habit(user_id, callback.bot)

        await callback.answer("🏵 +5 XP за завершение привычки!", show_alert=False)
        await callback.message.edit_text("Привычка завершена и сохранена в статистику!")
    except Exception as e:
        logger.exception(f"[{user_id}] Ошибка при завершении привычки habit_id={habit_id}: {e}")
        await callback.answer("Ошибка при завершении привычки", show_alert=True)

# 🔹 Отмена завершения — возвращаем карточку привычки
@router.callback_query(F.data.startswith("cancel_complete_"))
async def handle_cancel_complete(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    habit_id = int(callback.data.split("_")[-1])

    try:
        logger.info(f"[{user_id}] Отменил завершение привычки (habit_id={habit_id})")
        await render_habit_card(callback.message, user_id, habit_id)
    except Exception as e:
        logger.exception(f"[{user_id}] Ошибка при отмене завершения habit_id={habit_id}: {e}")
        await callback.answer("Ошибка при возврате карточки", show_alert=True)

# 🔹 Нажата кнопка "Продлить" — показать подтверждение
@router.callback_query(F.data.startswith("extend_habit_"))
async def handle_extend_request(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    habit_id = int(callback.data.split("_")[-1])

    try:
        habit = await get_habit_by_id(habit_id)
        if not habit:
            logger.error(f"[{user_id}] Привычка не найдена при попытке продлить (habit_id={habit_id})")
            await callback.message.edit_text("❌ Привычка не найдена.")
            return

        logger.info(f"[{user_id}] Запрос на продление привычки (habit_id={habit_id})")

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[ 
            InlineKeyboardButton(text="Да", callback_data=f"confirm_extend_{habit_id}"),
            InlineKeyboardButton(text="Нет", callback_data=f"cancel_complete_{habit_id}")
        ]])

        await callback.message.edit_text("Продлить привычку на 5 дней?", reply_markup=keyboard)

    except Exception as e:
        logger.exception(f"[{user_id}] Ошибка при обработке запроса на продление habit_id={habit_id}: {e}")
        await callback.answer("Ошибка при открытии продления", show_alert=True)

# 🔹 Подтверждение продления привычки
@router.callback_query(F.data.startswith("confirm_extend_"))
async def handle_confirm_extend(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    habit_id = int(callback.data.split("_")[-1])

    try:
        from services.profile import xp_service  # локальный импорт, чтобы избежать циклических импортов

        await extend_habit_by_id(habit_id)
        logger.info(f"[{user_id}] Продлил привычку на 5 дней (habit_id={habit_id})")

        # Начисляем XP за продление привычки
        await xp_service.xp_for_extend_habit(user_id, callback.bot)

        await callback.answer("🏵 +2 XP за продление привычки!", show_alert=False)

        await render_habit_card(callback.message, user_id, habit_id)
    except Exception as e:
        logger.exception(f"[{user_id}] Ошибка при подтверждении продления habit_id={habit_id}: {e}")
        await callback.answer("Не удалось продлить привычку", show_alert=True)
