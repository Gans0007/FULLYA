import logging
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from states.habit_states import HabitForm
from services.habits.habit_service import save_habit
from repositories.habits.habit_repo import count_user_habits
from handlers.achievements import check_and_grant
from db.db import database
from handlers.texts.habit_add_texts import HABIT_ADD_FSM

logger = logging.getLogger(__name__)
router = Router()


async def get_lang(user_id: int) -> str:
    row = await database.fetch_one("SELECT language FROM users WHERE user_id = :uid", {"uid": user_id})
    return row["language"] if row and row["language"] in HABIT_ADD_FSM else "ru"


# ✅ Обработка кнопки "➕ Добавить привычку"
@router.callback_query(lambda c: c.data == "add_habit_custom")
async def callback_start_habit(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = HABIT_ADD_FSM[lang]

    logger.info(f"[{user_id}] Нажал на ➕ Добавить привычку")

    total_habits = await count_user_habits(user_id)
    if total_habits >= 10:
        await callback.message.answer(t["add_limit_reached"])
        await callback.answer()
        return

    cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["btn_cancel"], callback_data="cancel_fsm_habit")]
    ])

    await callback.message.answer(t["enter_name"], reply_markup=cancel_kb)
    await state.set_state(HabitForm.name)
    await callback.answer()


@router.message(HabitForm.name)
async def process_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await get_lang(user_id)
    t = HABIT_ADD_FSM[lang]

    logger.info(f"[{user_id}] Ввел название привычки: {message.text}")
    await state.update_data(name=message.text)

    cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["btn_cancel"], callback_data="cancel_fsm_habit")]
    ])

    await message.answer(t["enter_days"], reply_markup=cancel_kb)
    await state.set_state(HabitForm.days)


@router.message(HabitForm.days)
async def process_days(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await get_lang(user_id)
    t = HABIT_ADD_FSM[lang]

    cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["btn_cancel"], callback_data="cancel_fsm_habit")]
    ])

    if not message.text.isdigit():
        logger.warning(f"[{user_id}] Ввел нецифровое значение дней: {message.text}")
        await message.answer(t["invalid_days"], reply_markup=cancel_kb)
        return

    logger.info(f"[{user_id}] Ввел длительность привычки: {message.text} дней")
    await state.update_data(days=int(message.text))
    await message.answer(t["enter_description"], reply_markup=cancel_kb)
    await state.set_state(HabitForm.description)


@router.message(HabitForm.description)
async def process_description(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await get_lang(user_id)
    t = HABIT_ADD_FSM[lang]

    await state.update_data(description=message.text)
    data = await state.get_data()

    logger.info(f"[{user_id}] Ввел описание привычки")

    summary = t["summary"].format(
        name=data["name"],
        days=data["days"],
        description=data["description"]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["btn_save"], callback_data="save_habit")],
        [InlineKeyboardButton(text=t["btn_delete"], callback_data="cancel_habit")]
    ])

    logger.info(f"[{user_id}] Подтвердительная карточка сформирована: {data}")
    await message.answer(summary, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(lambda c: c.data == "save_habit")
async def confirm_habit(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = HABIT_ADD_FSM[lang]

    data = await state.get_data()
    logger.info(f"[{user_id}] Подтверждает сохранение привычки: {data}")

    try:
        await save_habit(
            user_id=user_id,
            name=data["name"],
            days=int(data["days"]),
            description=data["description"]
        )

        total_habits = await count_user_habits(user_id)
        await check_and_grant(user_id, "habit_create", total_habits, callback.bot)

        await callback.message.edit_text(t["save_success"])
        logger.info(f"[{user_id}] Привычка сохранена успешно в БД")

    except Exception as e:
        logger.exception(f"[{user_id}] Ошибка при сохранении привычки: {e}")
        await callback.message.edit_text(t["save_error"].format(error=e))

    finally:
        await state.clear()
        await callback.answer()


@router.callback_query(lambda c: c.data == "cancel_habit")
async def cancel_habit(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = HABIT_ADD_FSM[lang]

    logger.info(f"[{user_id}] Отменил создание привычки (финальный этап)")
    await state.clear()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["btn_add"], callback_data="add_habit_custom")],
        [InlineKeyboardButton(text=t["btn_challenge"], callback_data="take_challenge")]
    ])

    await callback.message.edit_text(t["cancelled"], reply_markup=keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data == "cancel_fsm_habit")
async def cancel_fsm_creation(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = HABIT_ADD_FSM[lang]

    logger.info(f"[{user_id}] Отменил FSM-добавление привычки")
    await state.clear()
    await callback.message.edit_text(t["fsm_cancelled"])
    await callback.answer()
