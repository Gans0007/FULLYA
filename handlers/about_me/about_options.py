# handlers/about_me/about_options.py

from aiogram import Router, types, F, Bot
from aiogram.types import CallbackQuery
from db.db import database
from handlers.about_me.about_menu import get_about_inline_menu
from handlers.texts.about_me import NOTIFICATION_TONES, ABOUT_OPTIONS_TEXTS
from keyboards.menu import get_main_menu
from handlers.texts.menu_texts import MAIN_MENU_TEXTS

router = Router()


@router.callback_query(F.data == "about_options")
async def show_about_options(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Язык пользователя (fallback: ru)
    lang = await database.fetch_val(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id}
    ) or "ru"
    texts = ABOUT_OPTIONS_TEXTS.get(lang, ABOUT_OPTIONS_TEXTS["ru"])

    # Тон уведомлений (fallback: mixed)
    tone_code = await database.fetch_val(
        "SELECT notification_tone FROM users WHERE user_id = :uid",
        {"uid": user_id}
    ) or "mixed"
    tone_label = NOTIFICATION_TONES.get(tone_code, {}).get(lang, texts["btn_tone_mixed"])

    # Бейдж языка для шапки
    lang_badge_map = texts.get("lang_badge", {"ru": "RU", "uk": "UK", "en": "EN"})
    lang_label = lang_badge_map.get(lang, lang_badge_map.get("ru", "RU"))

    # Флаг публикации медиа в общий чат (fallback: True)
    share_on = await database.fetch_val(
        "SELECT share_confirmation_media FROM users WHERE user_id = :uid",
        {"uid": user_id}
    )
    if share_on is None:
        share_on = True

    # Текст кнопки-тумблера
    btn_share_on = texts.get("btn_share_on", "Вкл 🟢")
    btn_share_off = texts.get("btn_share_off", "Выкл ⚪")
    share_btn_text = btn_share_on if share_on else btn_share_off

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=texts["btn_tone_soft"], callback_data="tone_soft"),
            types.InlineKeyboardButton(text=texts["btn_tone_hard"], callback_data="tone_hard"),
            types.InlineKeyboardButton(text=texts["btn_tone_mixed"], callback_data="tone_mixed"),
        ],
        [
            types.InlineKeyboardButton(text=texts["btn_lang_uk"], callback_data="lang_uk"),
            types.InlineKeyboardButton(text=texts["btn_lang_en"], callback_data="lang_en"),
            types.InlineKeyboardButton(text=texts["btn_lang_ru"], callback_data="lang_ru"),
        ],
        [
            types.InlineKeyboardButton(
                text=f"{texts.get('share_label', 'Публикация медиа в общий чат')}: {share_btn_text}",
                callback_data="toggle_share_media"
            )
        ],
        [types.InlineKeyboardButton(text=texts["btn_back"], callback_data="about_back")]
    ])

    await callback.message.answer(
        text=(
            f"<b>{texts['title']}</b>\n\n"
            f"{texts['description']}\n\n"
            f"{texts['notification_label']}: <b>{tone_label}</b>\n"
            f"{texts['language_label']}: <b>{lang_label}</b>\n"
            f"{texts.get('share_label', 'Публикация медиа в общий чат')}: "
            f"<b>{'ON' if share_on else 'OFF'}</b>"
        ),
        parse_mode="HTML",
        reply_markup=keyboard
    )



@router.callback_query(F.data.startswith("tone_"))
async def set_notification_tone(callback: CallbackQuery):
    user_id = callback.from_user.id
    tone_code = callback.data.replace("tone_", "")

    # Язык для локализации ответов
    lang = await database.fetch_val(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id}
    ) or "ru"
    texts = ABOUT_OPTIONS_TEXTS.get(lang, ABOUT_OPTIONS_TEXTS["ru"])

    if tone_code not in NOTIFICATION_TONES:
        await callback.answer(texts["error_invalid_choice"], show_alert=True)
        return

    await database.execute(
        "UPDATE users SET notification_tone = :tone WHERE user_id = :uid",
        {"tone": tone_code, "uid": user_id}
    )

    await callback.answer(texts["tone_updated"])
    await show_about_options(callback)


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    lang_code = callback.data.replace("lang_", "")

    # Текущий язык для локализации ответов до переключения
    current_lang = await database.fetch_val(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id}
    ) or "ru"
    texts = ABOUT_OPTIONS_TEXTS.get(current_lang, ABOUT_OPTIONS_TEXTS["ru"])

    if lang_code not in ["ru", "uk", "en"]:
        await callback.answer(texts["error_invalid_lang"], show_alert=True)
        return

    # Обновляем язык
    await database.execute(
        "UPDATE users SET language = :lang WHERE user_id = :uid",
        {"lang": lang_code, "uid": user_id}
    )

    # Сообщаем об успехе на старом языке
    await callback.answer(texts["lang_updated"])

    # Обновляем главное меню сразу (на новом языке)
    await callback.message.answer(
        text=MAIN_MENU_TEXTS[lang_code]["language_changed"],
        reply_markup=get_main_menu(lang_code)
    )

    # Перерисовываем настройки (уже на новом языке)
    await show_about_options(callback)


@router.callback_query(F.data == "toggle_share_media")
async def toggle_share_media(callback: CallbackQuery):
    user_id = callback.from_user.id

    lang = await database.fetch_val(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id}
    ) or "ru"
    texts = ABOUT_OPTIONS_TEXTS.get(lang, ABOUT_OPTIONS_TEXTS["ru"])

    current = await database.fetch_val(
        "SELECT share_confirmation_media FROM users WHERE user_id = :uid",
        {"uid": user_id}
    )
    if current is None:
        current = True

    new_value = not current
    await database.execute(
        "UPDATE users SET share_confirmation_media = :v WHERE user_id = :uid",
        {"v": new_value, "uid": user_id}
    )

    await callback.answer(texts["share_updated"])
    await show_about_options(callback)
