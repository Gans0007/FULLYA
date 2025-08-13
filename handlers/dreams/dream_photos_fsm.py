from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.ui import try_edit_message
from db.db import database
from handlers.texts.dreams_texts import DREAMS_ADD_PHOTO_FSM_TEXTS
import logging
import os

logger = logging.getLogger(__name__)
router = Router()

class DreamPhotoFSM(StatesGroup):
    choosing_dream = State()
    waiting_for_photo = State()

async def get_lang(user_id: int) -> str:
    row = await database.fetch_one("SELECT language FROM users WHERE user_id = :uid", {"uid": user_id})
    return row["language"] if row and row["language"] in DREAMS_ADD_PHOTO_FSM_TEXTS else "ru"

@router.callback_query(F.data == "start_add_dream_photo")
async def start_photo_addition(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = DREAMS_ADD_PHOTO_FSM_TEXTS[lang]

    logger.info(f"[PLANS & DREAMS] ▶️ Пользователь {user_id} начал добавление фото к мечте")

    try:
        dreams = await database.fetch_all(
            """
            SELECT id, text 
            FROM dreams 
            WHERE user_id = :uid AND is_done = false
            """,
            {"uid": user_id}
        )
    except Exception as e:
        logger.error(f"[PLANS & DREAMS] Ошибка при загрузке мечт: {e}")
        await callback.answer(t["error_loading_dreams"], show_alert=True)
        return

    if not dreams:
        await callback.answer(t["no_active_dreams"], show_alert=True)
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=dream["text"][:40], callback_data=f"select_dream_{dream['id']}")]
            for dream in dreams
        ]
    )

    await state.set_state(DreamPhotoFSM.choosing_dream)
    await callback.message.answer(t["select_dream_prompt"], reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.func(lambda d: d.startswith("select_dream_")), DreamPhotoFSM.choosing_dream)
async def choose_dream(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = DREAMS_ADD_PHOTO_FSM_TEXTS[lang]

    dream_id = int(callback.data.split("_")[-1])
    logger.info(f"[PLANS & DREAMS] Пользователь {user_id} выбрал мечту ID={dream_id}")

    await state.update_data(dream_id=dream_id)
    await state.set_state(DreamPhotoFSM.waiting_for_photo)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t["cancel_button"], callback_data="cancel_add_dream_photo")]]
    )

    await try_edit_message(callback, text=t["send_photo_prompt"], markup=markup)
    await callback.answer()

@router.message(DreamPhotoFSM.waiting_for_photo, F.photo)
async def handle_dream_photo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await get_lang(user_id)
    t = DREAMS_ADD_PHOTO_FSM_TEXTS[lang]

    data = await state.get_data()
    dream_id = data.get("dream_id")

    photo = message.photo[-1]
    file_unique_id = photo.file_unique_id

    save_dir = "media/dreams"
    os.makedirs(save_dir, exist_ok=True)
    save_path = f"{save_dir}/{file_unique_id}.jpg"

    try:
        file_stream = await message.bot.download(photo.file_id)
        with open(save_path, "wb") as f:
            f.write(file_stream.read())
    except Exception as e:
        logger.error(f"Ошибка сохранения фото: {e}")
        await message.answer(t["photo_save_error"])
        return

    count_row = await database.fetch_one(
        "SELECT COUNT(*) FROM dream_photos WHERE dream_id = :did",
        {"did": dream_id}
    )
    count = list(count_row.values())[0] if count_row else 0
    if count >= 3:
        await message.answer(t["photo_limit"])
        return

    await database.execute(
        """
        INSERT INTO dream_photos (user_id, dream_id, photo_path) 
        VALUES (:uid, :did, :path)
        """,
        {"uid": user_id, "did": dream_id, "path": save_path}
    )

    await message.answer(t["photo_success"])
    await state.clear()

@router.callback_query(F.data == "cancel_add_dream_photo")
async def cancel_add_dream_photo(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    t = DREAMS_ADD_PHOTO_FSM_TEXTS[lang]

    await state.clear()
    await callback.message.answer(t["cancel_success"])
    await callback.answer()
