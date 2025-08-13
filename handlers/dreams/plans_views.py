from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils.ui import try_edit_message, safe_replace_message
from db.db import database
from handlers.texts.dreams_texts import PLANS_VIEW_TEXTS
import logging

logger = logging.getLogger(__name__)
router = Router()


async def get_lang(user_id: int) -> str:
    try:
        row = await database.fetch_one("SELECT language FROM users WHERE user_id = :uid", {"uid": user_id})
        return row["language"] if row and row["language"] in PLANS_VIEW_TEXTS else "ru"
    except Exception as e:
        logger.exception(f"[PLANS] Ошибка при получении языка пользователя {user_id}: {e}")
        return "ru"


@router.callback_query(F.data == "view_plans")
async def view_plans(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = PLANS_VIEW_TEXTS[lang]

    logger.info(f"[PLANS] Пользователь {user_id} открыл список планов")

    try:
        plans = await database.fetch_all(
            "SELECT id, goal_id, text, is_done FROM plans WHERE user_id = :uid",
            {"uid": user_id}
        )

        if not plans:
            logger.info(f"[PLANS] У пользователя {user_id} нет планов")
            await callback.answer(t["no_plans"])
            return

        grouped = {}
        for p in plans:
            grouped.setdefault(p["goal_id"], []).append((p["text"], p["is_done"]))

        goals = await database.fetch_all(
            "SELECT id, text FROM goals WHERE user_id = :uid",
            {"uid": user_id}
        )
        goal_dict = {g["id"]: g["text"] for g in goals}

        text = t["title"]
        for goal_id, plan_list in grouped.items():
            goal_title = goal_dict.get(goal_id, "Без цели")
            text += t["goal_prefix"].format(goal_title=goal_title)
            for plan_text, is_done in plan_list:
                display_text = f"<s>{plan_text}</s>" if is_done else plan_text
                text += f"  • {display_text}\n"
            text += "\n"

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=t["complete_button"], callback_data="choose_plan_to_complete"),
                InlineKeyboardButton(text=t["delete_button"], callback_data="choose_plan_to_delete")
            ],
            [
                InlineKeyboardButton(text=t["edit_button"], callback_data="choose_plan_to_edit"),
                InlineKeyboardButton(text=t["back_button"], callback_data="back_to_dreams_plans_menu")
            ]
        ])

        await try_edit_message(callback, text=text, markup=markup, parse_mode="HTML")
        await callback.answer()
    except Exception as e:
        logger.exception(f"[PLANS] Ошибка при отображении планов пользователя {user_id}: {e}")
        await callback.answer("⚠️ Ошибка при загрузке списка планов.")


@router.callback_query(F.data == "choose_plan_to_complete")
async def choose_plan_to_complete(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = PLANS_VIEW_TEXTS[lang]

    try:
        plans = await database.fetch_all(
            "SELECT id, text, is_done FROM plans WHERE user_id = :uid",
            {"uid": user_id}
        )

        if not plans:
            logger.info(f"[PLANS] Нет планов для завершения у пользователя {user_id}")
            await callback.answer(t["no_plans_to_complete"])
            return

        keyboard = [
            [InlineKeyboardButton(text=f"{'✅ ' if p['is_done'] else ''}{p['text']}", callback_data=f"toggle_plan_{p['id']}")]
            for p in plans
        ]
        keyboard.append([InlineKeyboardButton(text=t["back_button"], callback_data="view_plans")])

        await try_edit_message(callback, text=t["choose_for_complete"], markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
        await callback.answer()
    except Exception as e:
        logger.exception(f"[PLANS] Ошибка при выборе планов для завершения у пользователя {user_id}: {e}")
        await callback.answer("⚠️ Ошибка при загрузке списка.")


@router.callback_query(F.data.startswith("toggle_plan_"))
async def toggle_plan_status(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = PLANS_VIEW_TEXTS[lang]
    plan_id = int(callback.data.split("_")[-1])

    try:
        row = await database.fetch_one(
            "SELECT is_done FROM plans WHERE id = :id AND user_id = :uid",
            {"id": plan_id, "uid": user_id}
        )
        if not row:
            logger.warning(f"[PLANS] План {plan_id} не найден у пользователя {user_id}")
            await callback.answer(t["plan_not_found"])
            return

        new_status = not row["is_done"]
        await database.execute(
            "UPDATE plans SET is_done = :new_status WHERE id = :id",
            {"new_status": new_status, "id": plan_id}
        )

        logger.info(f"[PLANS] Пользователь {user_id} переключил статус плана {plan_id} на {new_status}")
        await choose_plan_to_complete(callback)
    except Exception as e:
        logger.exception(f"[PLANS] Ошибка при переключении статуса плана {plan_id} у пользователя {user_id}: {e}")
        await callback.answer("⚠️ Не удалось обновить статус.")


@router.callback_query(F.data == "choose_plan_to_delete")
async def choose_plan_to_delete(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = PLANS_VIEW_TEXTS[lang]

    try:
        plans = await database.fetch_all(
            "SELECT id, text, is_done FROM plans WHERE user_id = :uid",
            {"uid": user_id}
        )

        if not plans:
            logger.info(f"[PLANS] Нет планов для удаления у пользователя {user_id}")
            await callback.answer(t["no_plans_to_delete"])
            return

        keyboard = [
            [InlineKeyboardButton(text=f"{'✅ ' if p['is_done'] else ''}{p['text']}", callback_data=f"delete_plan_{p['id']}")]
            for p in plans
        ]
        keyboard.append([InlineKeyboardButton(text=t["back_button"], callback_data="view_plans")])

        await try_edit_message(callback, text=t["choose_for_delete"], markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
        await callback.answer()
    except Exception as e:
        logger.exception(f"[PLANS] Ошибка при выборе планов для удаления у пользователя {user_id}: {e}")
        await callback.answer("⚠️ Ошибка при отображении планов.")


@router.callback_query(F.data.startswith("delete_plan_"))
async def delete_plan(callback: CallbackQuery):
    user_id = callback.from_user.id
    plan_id = int(callback.data.split("_")[-1])
    lang = await get_lang(user_id)
    t = PLANS_VIEW_TEXTS[lang]

    try:
        await database.execute(
            "DELETE FROM plans WHERE id = :id AND user_id = :uid",
            {"id": plan_id, "uid": user_id}
        )

        logger.info(f"[PLANS] Пользователь {user_id} удалил план {plan_id}")

        count_row = await database.fetch_one(
            "SELECT COUNT(*) FROM plans WHERE user_id = :uid",
            {"uid": user_id}
        )
        count = list(count_row.values())[0]
        if count == 0:
            await safe_replace_message(callback.message, t["plan_deleted_last"], parse_mode="HTML")
        else:
            await callback.answer(t["plan_deleted"])
            await choose_plan_to_delete(callback)
    except Exception as e:
        logger.exception(f"[PLANS] Ошибка при удалении плана {plan_id} у пользователя {user_id}: {e}")
        await callback.answer("⚠️ Ошибка при удалении.")
