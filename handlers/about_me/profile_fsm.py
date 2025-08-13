import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.profile_states import ProfileStates
from repositories.profiles.profile_repository import (
    save_profile,
    get_profile,
    update_profile_field,
)
from utils.ui import safe_replace_message
from .profile_view import show_profile  # возврат в профиль после отмены/сохранения

# ⬇️ мультиязычные тексты и язык пользователя
from handlers.texts.about_me import PROFILE_FSM_TEXTS
from db.db import database

logger = logging.getLogger(__name__)
router = Router()

# Простое временное хранилище выбора поля
edit_profile_state: dict[int, str] = {}


async def get_lang(user_id: int) -> str:
    """Возвращает язык интерфейса пользователя с fallback на 'ru'."""
    row = await database.fetch_one(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id},
    )
    if not row:
        return "ru"
    try:
        lang = row["language"]
    except Exception:
        return "ru"
    return lang if lang in PROFILE_FSM_TEXTS else "ru"


@router.callback_query(F.data == "edit_profile")
async def edit_profile(callback: types.CallbackQuery, state: FSMContext):
    """Редактирование профиля: открывает меню или запускает создание"""
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    T = PROFILE_FSM_TEXTS[lang]

    logger.info(f"[PROFILE] Пользователь {user_id} открыл редактирование профиля")
    profile = await get_profile(user_id)

    # Если профиля нет — запускаем пошаговое создание через FSM
    if not profile:
        builder = InlineKeyboardBuilder()
        builder.button(text=T["cancel"], callback_data="cancel_profile_edit")
        await callback.message.answer(T["start_name"], reply_markup=builder.as_markup())
        await state.set_state(ProfileStates.name)
        return

    # Есть профиль — даём выбрать конкретное поле
    builder = InlineKeyboardBuilder()
    builder.button(text=T["fields"]["name"], callback_data="edit_name")
    builder.button(text=T["fields"]["age"], callback_data="edit_age")
    builder.button(text=T["fields"]["specialization"], callback_data="edit_specialization")
    builder.button(text=T["fields"]["help"], callback_data="edit_help")
    builder.button(text=T["fields"]["message"], callback_data="edit_message")
    builder.adjust(2)

    await callback.answer()
    await callback.message.answer(T["select_field"], reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("edit_"))
async def handle_field_choice(callback: types.CallbackQuery):
    """Выбор поля для точечного редактирования"""
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    T = PROFILE_FSM_TEXTS[lang]

    field = callback.data.replace("edit_", "")
    edit_profile_state[user_id] = field
    logger.info(
        f"[PROFILE] Пользователь {user_id} выбрал поле для редактирования: {field}"
    )

    prompts = T["prompts"]
    builder = InlineKeyboardBuilder()
    builder.button(text=T["cancel"], callback_data="cancel_profile_edit")
    await callback.answer()
    await callback.message.answer(prompts[field], reply_markup=builder.as_markup())


@router.callback_query(F.data == "cancel_profile_edit")
async def cancel_profile_edit(callback: types.CallbackQuery, state: FSMContext):
    """Отмена редактирования/создания"""
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    T = PROFILE_FSM_TEXTS[lang]

    await state.clear()
    edit_profile_state.pop(user_id, None)
    await callback.message.answer(T["cancelled"])
    await show_profile(callback)


@router.message(F.text)  # не ловим всё подряд, только текст
async def handle_field_input(message: types.Message, state: FSMContext):
    """Обработка ввода данных: точечное редактирование и пошаговое создание"""
    user_id = message.from_user.id
    lang = await get_lang(user_id)
    T = PROFILE_FSM_TEXTS[lang]

    # ===== Точечное редактирование выбранного поля =====
    if user_id in edit_profile_state:
        field = edit_profile_state.pop(user_id)
        value = message.text.strip()

        # Валидация
        if field == "age":
            try:
                value = int(value)
            except ValueError:
                await message.answer(T["errors"]["age"])
                return
        elif field == "specialization" and len(value) > 15:
            await message.answer(T["errors"]["specialization"])
            return
        elif field == "help" and len(value) > 70:
            await message.answer(T["errors"]["help"])
            return
        elif field == "message" and len(value) > 60:
            await message.answer(T["errors"]["message"])
            return

        await update_profile_field(
            user_id, field, value, message.from_user.username or ""
        )
        builder = InlineKeyboardBuilder()
        builder.button(text=T["view_changes"], callback_data="about_profile")
        await message.answer(T["updated"], reply_markup=builder.as_markup())
        return

    # ===== Пошаговое создание профиля через FSM =====
    current_state = await state.get_state()

    if current_state == ProfileStates.name:
        await state.update_data(name=message.text)
        builder = InlineKeyboardBuilder()
        builder.button(text=T["cancel"], callback_data="cancel_profile_edit")
        await message.answer(T["step_age"], reply_markup=builder.as_markup())
        await state.set_state(ProfileStates.age)
        return

    if current_state == ProfileStates.age:
        try:
            age = int(message.text)
        except ValueError:
            logger.warning(f"[PROFILE] Некорректный ввод возраста: {message.text}")
            await message.answer(T["errors"]["age"])
            return
        await state.update_data(age=age)
        builder = InlineKeyboardBuilder()
        builder.button(text=T["cancel"], callback_data="cancel_profile_edit")
        await message.answer(T["step_spec"], reply_markup=builder.as_markup())
        await state.set_state(ProfileStates.specialization)
        return

    if current_state == ProfileStates.specialization:
        await state.update_data(specialization=message.text)
        builder = InlineKeyboardBuilder()
        builder.button(text=T["cancel"], callback_data="cancel_profile_edit")
        await message.answer(T["step_help"], reply_markup=builder.as_markup())
        await state.set_state(ProfileStates.help_text)
        return

    if current_state == ProfileStates.help_text:
        await state.update_data(help_text=message.text)
        builder = InlineKeyboardBuilder()
        builder.button(text=T["cancel"], callback_data="cancel_profile_edit")
        await message.answer(T["step_message"], reply_markup=builder.as_markup())
        await state.set_state(ProfileStates.message)
        return

    if current_state == ProfileStates.message:
        data = await state.update_data(message=message.text)
        await save_profile(
            user_id=user_id,
            name=data["name"],
            username=message.from_user.username or "",
            age=data["age"],
            specialization=data["specialization"],
            help_text=data["help_text"],
            message=data["message"],
        )
        await state.clear()
        logger.info(f"[PROFILE] Пользователь {user_id} успешно создал профиль")
        await message.answer(T["created"])
        return
