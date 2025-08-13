from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, InputMediaPhoto
from utils.ui import try_edit_message, safe_replace_message
from db.db import database
from handlers.texts.dreams_texts import DREAMS_VIEW_TEXTS
import os

router = Router()

async def get_lang(user_id: int) -> str:
    row = await database.fetch_one("SELECT language FROM users WHERE user_id = :uid", {"uid": user_id})
    return row["language"] if row and row["language"] in DREAMS_VIEW_TEXTS else "ru"

@router.callback_query(F.data == "view_dreams")
async def view_dreams(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = DREAMS_VIEW_TEXTS[lang]

    all_dreams = await database.fetch_all(
        """
        SELECT id, text, is_done FROM dreams 
        WHERE user_id = :uid AND is_done = false ORDER BY id DESC
        """,
        {"uid": user_id}
    )

    all_photos = await database.fetch_all(
        "SELECT dream_id, photo_path FROM dream_photos WHERE user_id = :uid",
        {"uid": user_id}
    )

    if not all_dreams:
        await callback.answer(t["no_dreams"])
        return

    await callback.message.delete()
    await callback.answer()

    photo_mapping = {}
    for row in all_photos:
        dream_id, path = row["dream_id"], row["photo_path"]
        if os.path.exists(path):
            photo_mapping.setdefault(dream_id, []).append(path)

    dreams_with_photos = [d for d in all_dreams if d["id"] in photo_mapping]
    dreams_without_photos = [d for d in all_dreams if d["id"] not in photo_mapping]

    for d in dreams_with_photos:
        photos = photo_mapping[d["id"]]
        media = []
        for i, path in enumerate(photos):
            file = FSInputFile(path)
            if i == 0:
                media.append(InputMediaPhoto(media=file, caption=f"💭 <b>{d['text']}</b>", parse_mode="HTML"))
            else:
                media.append(InputMediaPhoto(media=file))

        await callback.bot.send_media_group(chat_id=user_id, media=media)

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=t["buttons"]["dream_done"], callback_data=f"set_dream_done_{d['id']}"),
                InlineKeyboardButton(text=t["buttons"]["delete"], callback_data=f"confirm_delete_dream_{d['id']}")
            ]
        ])
        await callback.bot.send_message(chat_id=user_id, text=t["actions_prompt"], reply_markup=markup)

    if dreams_without_photos:
        text = t["dreams_no_photos_title"]
        for d in dreams_without_photos:
            text += t["dreams_no_photos_line"].format(dream_text=d["text"])

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=t["buttons"]["dream_done"], callback_data="mark_dream_done"),
                InlineKeyboardButton(text=t["buttons"]["add_photo"], callback_data="start_add_dream_photo")
            ],
            [
                InlineKeyboardButton(text=t["buttons"]["delete"], callback_data="delete_dream_menu"),
                InlineKeyboardButton(text=t["buttons"]["back"], callback_data="back_to_dreams_plans_menu")
            ]
        ])

        await callback.bot.send_message(chat_id=user_id, text=text, reply_markup=markup, parse_mode="HTML")


@router.callback_query(F.data == "mark_dream_done")
async def mark_dream_done_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = DREAMS_VIEW_TEXTS[lang]

    dreams = await database.fetch_all(
        "SELECT id, text FROM dreams WHERE user_id = :uid AND is_done = false",
        {"uid": user_id}
    )

    if not dreams:
        await callback.answer(t["no_active_dreams"])
        return

    keyboard = [
        [InlineKeyboardButton(text=d["text"], callback_data=f"set_dream_done_{d['id']}")]
        for d in dreams
    ]
    keyboard.append([InlineKeyboardButton(text=t["buttons"]["back"], callback_data="view_dreams")])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await try_edit_message(callback, text=t["choose_dream_done"], markup=markup)
    await callback.answer()


@router.callback_query(F.data == "delete_dream_menu")
async def show_dreams_to_delete(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = DREAMS_VIEW_TEXTS[lang]

    dreams = await database.fetch_all(
        "SELECT id, text FROM dreams WHERE user_id = :uid AND is_done = false",
        {"uid": user_id}
    )

    dreams_with_photos = await database.fetch_all(
        "SELECT DISTINCT dream_id FROM dream_photos WHERE user_id = :uid",
        {"uid": user_id}
    )
    dreams_with_photos = {row["dream_id"] for row in dreams_with_photos}
    dreams_without_photos = [d for d in dreams if d["id"] not in dreams_with_photos]

    if not dreams_without_photos:
        await callback.answer(t["no_dreams_to_delete"])
        return

    keyboard = [
        [InlineKeyboardButton(text=d["text"], callback_data=f"delete_dream_{d['id']}")]
        for d in dreams_without_photos
    ]
    keyboard.append([InlineKeyboardButton(text=t["buttons"]["back"], callback_data="view_dreams")])

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.answer(t["choose_dream_to_delete"], reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("delete_dream_"))
async def delete_dream(callback: CallbackQuery):
    dream_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = DREAMS_VIEW_TEXTS[lang]

    await database.execute("DELETE FROM dreams WHERE id = :id AND user_id = :uid",
                           {"id": dream_id, "uid": user_id})
    await database.execute("DELETE FROM dream_photos WHERE dream_id = :id", {"id": dream_id})

    await safe_replace_message(callback.message, t["dream_deleted"])
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_delete_dream_"))
async def confirm_delete_dream(callback: CallbackQuery):
    dream_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = DREAMS_VIEW_TEXTS[lang]

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t["buttons"]["yes"], callback_data=f"delete_photo_dream_{dream_id}"),
            InlineKeyboardButton(text=t["buttons"]["no"], callback_data="view_dreams")
        ]
    ])
    await try_edit_message(callback, text=t["confirm_delete"], markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("delete_photo_dream_"))
async def delete_photo_dream(callback: CallbackQuery):
    dream_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = DREAMS_VIEW_TEXTS[lang]

    rows = await database.fetch_all(
        "SELECT photo_path FROM dream_photos WHERE dream_id = :id",
        {"id": dream_id}
    )
    for r in rows:
        path = r["photo_path"]
        if os.path.exists(path):
            os.remove(path)

    await database.execute("DELETE FROM dream_photos WHERE dream_id = :id", {"id": dream_id})
    await database.execute("DELETE FROM dreams WHERE id = :id AND user_id = :uid",
                           {"id": dream_id, "uid": user_id})

    await safe_replace_message(callback.message, t["dream_deleted_with_photos"])
    await callback.answer()


@router.callback_query(F.data.startswith("set_dream_done_"))
async def set_dream_done(callback: CallbackQuery):
    dream_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    lang = await get_lang(user_id)
    t = DREAMS_VIEW_TEXTS[lang]

    await database.execute(
        """
        UPDATE dreams
        SET is_done = true, done_at = NOW()
        WHERE id = :id AND user_id = :uid
        """,
        {"id": dream_id, "uid": user_id}
    )

    await safe_replace_message(
        callback.message,
        t["dream_done"],
        parse_mode="HTML"
    )
    await callback.answer()