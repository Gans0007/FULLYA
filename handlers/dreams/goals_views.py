import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils.ui import try_edit_message, safe_replace_message
from db.db import database
from handlers.texts.dreams_texts import GOALS_VIEW_TEXTS

logger = logging.getLogger(__name__)
router = Router()


async def get_lang(user_id: int) -> str:
    try:
        row = await database.fetch_one("SELECT language FROM users WHERE user_id = :uid", {"uid": user_id})
        lang = row["language"] if row and row["language"] in GOALS_VIEW_TEXTS else "ru"
        logger.debug(f"[GOALS] Язык пользователя {user_id}: {lang}")
        return lang
    except Exception as e:
        logger.exception(f"[GOALS] ❌ Ошибка при получении языка пользователя {user_id}: {e}")
        return "ru"


# 🎯 Мои цели
@router.callback_query(F.data == "view_goals")
async def view_goals(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.info(f"[GOALS] ▶️ Пользователь {user_id} открыл список целей")

    try:
        lang = await get_lang(user_id)
        text_data = GOALS_VIEW_TEXTS[lang]

        goals = await database.fetch_all(
            "SELECT text, is_done FROM goals WHERE user_id = :uid",
            {"uid": user_id}
        )

        if not goals:
            logger.info(f"[GOALS] У пользователя {user_id} нет целей")
            await callback.answer(text_data["no_goals"])
            return

        logger.info(f"[GOALS] Найдено {len(goals)} целей для пользователя {user_id}")

        text = text_data["title"]
        for g in goals:
            status = text_data["status_done"] if g["is_done"] else text_data["status_active"]
            text += f"• {g['text']} — {status}\n"

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=text_data["complete_button"], callback_data="choose_goal_to_complete"),
                InlineKeyboardButton(text=text_data["delete_button"], callback_data="choose_goal_to_delete")
            ],
            [
                InlineKeyboardButton(text=text_data["edit_button"], callback_data="choose_goal_to_edit"),
                InlineKeyboardButton(text=text_data["back_button"], callback_data="back_to_dreams_plans_menu")
            ]
        ])

        await safe_replace_message(callback.message, text, reply_markup=markup, parse_mode="HTML")
        await callback.answer()

    except Exception as e:
        logger.exception(f"[GOALS] ❌ Ошибка при отображении целей для пользователя {user_id}: {e}")
        await callback.answer("❌ Ошибка при загрузке целей.")


# ✅ Завершение цели
@router.callback_query(F.data.startswith("complete_goal_"))
async def complete_goal(callback: CallbackQuery):
    user_id = callback.from_user.id
    goal_id = int(callback.data.split("_")[-1])
    logger.info(f"[GOALS] ✅ Пользователь {user_id} завершает цель ID={goal_id}")

    try:
        lang = await get_lang(user_id)
        text_data = GOALS_VIEW_TEXTS[lang]

        await database.execute(
            "UPDATE goals SET is_done = true, done_at = NOW() WHERE id = :id",
            {"id": goal_id}
        )

        await try_edit_message(callback, text=text_data["goal_completed"])
        await callback.answer(text_data["goal_completed_alert"])

    except Exception as e:
        logger.exception(f"[GOALS] ❌ Ошибка при завершении цели ID={goal_id} пользователем {user_id}: {e}")
        await callback.answer("❌ Не удалось завершить цель.")


# 📋 Выбор цели для завершения
@router.callback_query(F.data == "choose_goal_to_complete")
async def choose_goal_to_complete(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.info(f"[GOALS] Пользователь {user_id} выбирает цель для завершения")

    try:
        lang = await get_lang(user_id)
        text_data = GOALS_VIEW_TEXTS[lang]

        goals = await database.fetch_all(
            "SELECT id, text FROM goals WHERE user_id = :uid AND is_done = false",
            {"uid": user_id}
        )

        if not goals:
            logger.info(f"[GOALS] У пользователя {user_id} нет активных целей")
            await callback.answer(text_data["no_active_goals"])
            return

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=g["text"], callback_data=f"complete_goal_{g['id']}")]
            for g in goals
        ])

        await try_edit_message(callback, text=text_data["choose_goal_to_complete"], markup=keyboard)
        await callback.answer()

    except Exception as e:
        logger.exception(f"[GOALS] ❌ Ошибка при выборе цели для завершения у пользователя {user_id}: {e}")
        await callback.answer("❌ Не удалось загрузить цели.")


# ❌ Выбор цели для удаления
@router.callback_query(F.data == "choose_goal_to_delete")
async def choose_goal_to_delete(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.info(f"[GOALS] Пользователь {user_id} выбирает цель для удаления")

    try:
        lang = await get_lang(user_id)
        text_data = GOALS_VIEW_TEXTS[lang]

        goals = await database.fetch_all(
            "SELECT id, text FROM goals WHERE user_id = :uid",
            {"uid": user_id}
        )

        if not goals:
            logger.info(f"[GOALS] У пользователя {user_id} нет целей для удаления")
            await callback.answer(text_data["no_goals_to_delete"])
            return

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=g["text"], callback_data=f"confirm_delete_goal_{g['id']}")]
            for g in goals
        ])

        await try_edit_message(callback, text=text_data["choose_goal_to_delete"], markup=keyboard)
        await callback.answer()

    except Exception as e:
        logger.exception(f"[GOALS] ❌ Ошибка при выборе цели для удаления у пользователя {user_id}: {e}")
        await callback.answer("❌ Ошибка при загрузке целей.")


# ✅ Подтверждение удаления цели
@router.callback_query(F.data.startswith("confirm_delete_goal_"))
async def delete_goal(callback: CallbackQuery):
    user_id = callback.from_user.id
    goal_id = int(callback.data.split("_")[-1])
    logger.info(f"[GOALS] 🗑 Пользователь {user_id} удаляет цель ID={goal_id}")

    try:
        lang = await get_lang(user_id)
        text_data = GOALS_VIEW_TEXTS[lang]

        await database.execute("DELETE FROM goals WHERE id = :id", {"id": goal_id})
        await try_edit_message(callback, text=text_data["goal_deleted"])
        await callback.answer(text_data["goal_deleted_alert"])

    except Exception as e:
        logger.critical(f"[GOALS] ❌ КРИТИЧЕСКАЯ ОШИБКА удаления цели ID={goal_id} пользователем {user_id}: {e}")
        await callback.answer("❌ Ошибка при удалении цели.")
