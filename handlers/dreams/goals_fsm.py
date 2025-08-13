from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.goals_states import GoalStates, PlanStates, DreamStates, GoalEditState
from handlers.dreams.goals_menu import handle_goals_menu
from utils.ui import try_edit_message
from db.db import database
from handlers.texts.dreams_texts import FSM_ADD_TEXTS
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = Router()

# ===== Helpers =====
async def get_lang(user_id: int) -> str:
    """Fetch user's language safely from DB.
    Avoid using dict-like .get() on Record: access by key.
    """
    row = await database.fetch_one(
        """
        SELECT COALESCE(language, 'ru') AS language
        FROM users
        WHERE user_id = :uid
        """,
        {"uid": user_id},
    )
    lang = row["language"] if row else "ru"
    return lang if lang in FSM_ADD_TEXTS else "ru"


def T(lang: str, key: str) -> str:
    base = FSM_ADD_TEXTS.get("ru", {})
    cur = FSM_ADD_TEXTS.get(lang, base)
    return cur.get(key, base.get(key, key))


def cancel_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=T(lang, "cancel_button"), callback_data="cancel_add_fsm")]]
    )


def choose_add_menu_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=T(lang, "goal_button"), callback_data="add_goal")],
            [InlineKeyboardButton(text=T(lang, "plan_button"), callback_data="add_plan")],
            [InlineKeyboardButton(text=T(lang, "dream_button"), callback_data="add_dream")],
            [InlineKeyboardButton(text=T(lang, "back_button"), callback_data="goals_menu")],
        ]
    )


# === START: Choose what to add ===
@router.callback_query(F.data == "add_new")
async def choose_what_to_add(callback: CallbackQuery):
    lang = await get_lang(callback.from_user.id)
    logger.info(f"[PLANS & DREAMS FSM] Пользователь {callback.from_user.id} открыл меню добавления.")
    await callback.message.answer(T(lang, "choose_what_to_add"), reply_markup=choose_add_menu_kb(lang))
    await callback.answer()


# === GOAL: Add ===
@router.callback_query(F.data == "add_goal")
async def add_goal_start(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    await callback.message.answer(T(lang, "ask_goal_text"), reply_markup=cancel_kb(lang))
    await state.set_state(GoalStates.waiting_for_goal_text)
    await callback.answer()


@router.message(GoalStates.waiting_for_goal_text)
async def add_goal_text(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    goal_text = (message.text or "").strip()
    user_id = message.from_user.id

    if not goal_text:
        await message.answer(T(lang, "empty_goal_error"))
        return

    try:
        await database.execute(
            """
            INSERT INTO goals (user_id, text, last_reminder)
            VALUES (:uid, :text, NOW())
            """,
            {"uid": user_id, "text": goal_text},
        )
    except Exception as e:
        logger.error(f"[PLANS & DREAMS FSM] Ошибка при добавлении цели: {e}")
        await message.answer(T(lang, "goal_save_error"))
        return

    await message.answer(T(lang, "goal_added").format(text=goal_text), parse_mode="HTML")
    await handle_goals_menu(message)
    await state.clear()


# === DREAM: Add ===
@router.callback_query(F.data == "add_dream")
async def add_dream_start(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    await callback.message.answer(T(lang, "ask_dream_text"), reply_markup=cancel_kb(lang))
    await state.set_state(DreamStates.waiting_for_dream_text)
    await callback.answer()


@router.message(DreamStates.waiting_for_dream_text)
async def add_dream_text(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    dream_text = (message.text or "").strip()
    user_id = message.from_user.id

    if not dream_text:
        await message.answer(T(lang, "empty_dream_error"))
        return

    try:
        await database.execute(
            """
            INSERT INTO dreams (user_id, text, is_done, last_reminder)
            VALUES (:uid, :text, :is_done, NOW())
            """,
            {"uid": user_id, "text": dream_text, "is_done": False},
        )
    except Exception as e:
        logger.error(f"[PLANS & DREAMS FSM] Ошибка при добавлении мечты: {e}")
        await message.answer(T(lang, "dream_save_error"))
        return

    await message.answer(T(lang, "dream_added").format(text=dream_text), parse_mode="HTML")
    await handle_goals_menu(message)
    await state.clear()


# === PLAN: Add ===
@router.callback_query(F.data == "add_plan")
async def ask_plan_binding(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=T(lang, "bind_yes"), callback_data="plan_bind_yes")],
            [InlineKeyboardButton(text=T(lang, "bind_no"), callback_data="plan_bind_no")],
        ]
    )
    await callback.message.answer(T(lang, "ask_plan_binding"), reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "plan_bind_yes")
async def choose_goal_for_plan(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    user_id = callback.from_user.id
    goals = await database.fetch_all(
        "SELECT id, text FROM goals WHERE user_id = :uid",
        {"uid": user_id},
    )
    if not goals:
        # Нет специального текста для этой ситуации в словаре — используем ближайший по смыслу
        await callback.message.answer(T(lang, "no_goals_to_edit"))
        await callback.answer()
        return

    buttons = [[InlineKeyboardButton(text=g["text"], callback_data=f"select_goal_{g['id']}")] for g in goals]
    await state.set_state(PlanStates.choosing_goal_link)
    await callback.message.answer(
        T(lang, "choose_goal_to_bind"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_goal_"))
async def ask_plan_text_with_goal(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    goal_id = int(callback.data.split("_")[-1])
    await state.update_data(goal_id=goal_id)
    await state.set_state(PlanStates.waiting_for_plan_text)
    await callback.message.answer(T(lang, "ask_plan_text"), reply_markup=cancel_kb(lang))
    await callback.answer()


@router.callback_query(F.data == "plan_bind_no")
async def skip_goal_and_ask_text(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    await state.update_data(goal_id=None)
    await state.set_state(PlanStates.waiting_for_plan_text)
    await callback.message.answer(T(lang, "ask_plan_text"), reply_markup=cancel_kb(lang))
    await callback.answer()


@router.message(PlanStates.waiting_for_plan_text)
async def save_plan(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    plan_text = (message.text or "").strip()
    user_id = message.from_user.id
    data = await state.get_data()
    goal_id = data.get("goal_id")

    if not plan_text:
        await message.answer(T(lang, "empty_plan_error"))
        return

    try:
        await database.execute(
            """
            INSERT INTO plans (user_id, goal_id, text)
            VALUES (:uid, :gid, :text)
            """,
            {"uid": user_id, "gid": goal_id, "text": plan_text},
        )
    except Exception as e:
        logger.error(f"[PLANS & DREAMS FSM] Ошибка при добавлении плана: {e}")
        await message.answer(T(lang, "plan_save_error"))
        return

    await message.answer(T(lang, "plan_added_linked") if goal_id else T(lang, "plan_added_unlinked"))
    await handle_goals_menu(message)
    await state.clear()


# === GOAL: Edit ===
@router.callback_query(F.data == "choose_goal_to_edit")
async def choose_goal_to_edit(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    user_id = callback.from_user.id
    goals = await database.fetch_all(
        "SELECT id, text FROM goals WHERE user_id = :uid",
        {"uid": user_id},
    )
    if not goals:
        await callback.answer(T(lang, "no_goals_to_edit"))
        return

    keyboard = [[InlineKeyboardButton(text=g["text"], callback_data=f"edit_goal_{g['id']}")] for g in goals]
    keyboard.append([InlineKeyboardButton(text=T(lang, "back_button"), callback_data="view_goals")])
    await state.set_state(GoalEditState.choosing_goal)
    await try_edit_message(
        callback,
        text=T(lang, "choose_goal_to_edit"),
        markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("edit_goal_"), GoalEditState.choosing_goal)
async def enter_new_goal_text(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    goal_id = int(callback.data.split("_")[-1])
    await state.update_data(goal_id=goal_id)
    await state.set_state(GoalEditState.waiting_for_new_text)
    await callback.message.answer(T(lang, "ask_new_goal_text"))
    await callback.answer()


@router.message(GoalEditState.waiting_for_new_text)
async def save_new_goal_text(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    new_text = (message.text or "").strip()
    data = await state.get_data()
    goal_id = data["goal_id"]

    if not new_text:
        await message.answer(T(lang, "empty_text_error"))
        return

    await database.execute(
        "UPDATE goals SET text = :text WHERE id = :id",
        {"text": new_text, "id": goal_id},
    )

    await message.answer(T(lang, "goal_updated"))
    await state.clear()
    await handle_goals_menu(message)


# === PLAN: Edit ===
@router.callback_query(F.data == "choose_plan_to_edit")
async def choose_plan_to_edit(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    user_id = callback.from_user.id
    plans = await database.fetch_all(
        "SELECT id, text FROM plans WHERE user_id = :uid",
        {"uid": user_id},
    )
    if not plans:
        await callback.answer(T(lang, "no_plans_to_edit"))
        return

    keyboard = [[InlineKeyboardButton(text=p["text"], callback_data=f"edit_plan_{p['id']}")] for p in plans]
    keyboard.append([InlineKeyboardButton(text=T(lang, "back_button"), callback_data="view_plans")])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await try_edit_message(callback, text=T(lang, "choose_plan_to_edit"), markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("edit_plan_"))
async def ask_new_plan_text(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    plan_id = int(callback.data.split("_")[-1])
    await state.update_data(plan_id=plan_id)
    await state.set_state(PlanStates.editing_plan)
    await callback.message.answer(T(lang, "ask_new_plan_text"))
    await callback.answer()


@router.message(PlanStates.editing_plan)
async def save_edited_plan(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    new_text = (message.text or "").strip()
    user_id = message.from_user.id
    data = await state.get_data()
    plan_id = data.get("plan_id")

    if not new_text:
        await message.answer(T(lang, "empty_text_error"))
        return

    await database.execute(
        "UPDATE plans SET text = :text WHERE id = :id AND user_id = :uid",
        {"text": new_text, "id": plan_id, "uid": user_id},
    )

    await message.answer(T(lang, "plan_updated"))
    await state.clear()
    await handle_goals_menu(message)


# === Cancel ===
@router.callback_query(F.data == "cancel_add_fsm")
async def cancel_fsm(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    await state.clear()
    await try_edit_message(callback, text=T(lang, "cancel_text"))
    await callback.answer()
